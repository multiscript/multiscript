
import logging
from operator import attrgetter
from pathlib import Path
from tempfile import TemporaryDirectory

import requests

from bibleref.ref import BibleRange, BibleRangeList
import fontfinder

import multiscript
from multiscript.bible.content import BibleContent
from multiscript.bible.version import BibleVersion
from multiscript.outputs.base import OutputPlanRun
from multiscript.plan import combinations, Plan
from multiscript.plan.combinations import BibleVersionCombo, BibleVersionColumn
from multiscript.plan.monitor import PlanMonitorCollection
from multiscript.util import serialize
from multiscript.util.exception import MultiscriptException

_logger = logging.getLogger(__name__)

# TODO: Make plan run record a hidden file on both macos and windows.
PLAN_RUN_RECORD_FILENAME = "_multiscript.mrun"


class PlanRunner:
    '''This class oversees the process of running a Plan: reading the Bible passages from the sources,
    and writing the Bible passages to the outputs.
    '''
    def __init__(self, plan, monitor=None):
        self.plan: Plan = plan
        self.monitors: PlanMonitorCollection = PlanMonitorCollection(self, monitor)
        self.total_progress_steps: int = 0
        self.progress_step_count: int = 0

        # BibleRangeList to be processed
        self.bible_ranges: BibleRangeList = BibleRangeList([])
        
        # Dict of all versions being used.
        # Keys: versions Vals: True (we're using the dict as an ordered set)
        self._all_versions: dict[BibleVersion, bool] = {}  
        
        # List of versions selected in each column
        self.version_cols: list[BibleVersionColumn] = []
        
        # Uses BibleVersions as keys to a list of BibleContents (one for each range in self.bible_ranges)
        self.bible_contents: dict[BibleVersion, list[BibleContent]] = {}    
        
        # FontFinder API object for font selection and installation.
        self.font_finder = fontfinder.FontFinder()

        # An empty object other classes may use for persisting data between plan runs with the same
        # output directory.
        self.run_record = PlanRunRecord()

        # Dict of OutputPlanRun by output long_id
        self.output_runs: dict[str, OutputPlanRun] = {}

        # A temporary directory made available during the plan run
        self.temp_dir_path = None
        
        #
        # Convert the data in the plan into the required form for this runner.
        #
        self.bible_ranges = BibleRangeList(plan.bible_passages)

        all_versions = plan.bible_versions
        for plan_version_column in plan.version_selection:
            column_version_list = []
            for row_index in range(len(plan_version_column)):
                if plan_version_column[row_index]:
                    column_version_list.append(all_versions[row_index])
            self._add_version_list(column_version_list)

        self.base_template_path = self.plan.template_abspath
        self.output_dir_path = self.plan.output_dir_abspath

        for output in multiscript.app().outputs_for_ext(self.base_template_path.suffix):
            self.output_runs[output.long_id] = output.new_output_plan_run(self.plan)

    def _add_version_list(self, version_list, symbol_index=None):
        for version in version_list:
            self._all_versions[version] = True
        if symbol_index is None:
            symbol_index = len(self.version_cols)
        self.version_cols.append(combinations.BibleVersionColumn(version_list, symbol_index))
        # For ease of display, sort the version_cols list by symbol index
        self.version_cols.sort(key=attrgetter('symbol_index'))

    @property
    def all_versions(self) -> list[BibleVersion]:
        return list(self._all_versions.keys())

    @property
    def all_version_combos(self) -> list[BibleVersionCombo]:
        return combinations.get_all_version_combos(self.version_cols)

    def run(self):
        self.output_dir_path.mkdir(parents=True, exist_ok=True)
        self.load_plan_run_record()
        
        with TemporaryDirectory() as temp_dir:
            self.temp_dir_path = Path(temp_dir)
            self.calc_total_progress_steps()
            self.load_bible_content()
            self.select_auto_fonts()
            self.download_and_install_fonts()
            self.create_bible_outputs()
        self.temp_dir_path = None
        
        self.save_plan_run_record()
        _logger.info("Finished")

    def load_plan_run_record(self):
        '''Load the PlanRunRecord. Called at the beginning of the plan run.'''
        record_path = self.output_dir_path / PLAN_RUN_RECORD_FILENAME
        if record_path.exists():
            self.run_record = serialize.load(record_path)
            _logger.info("\t\tFound existing plan run record.")

    def save_plan_run_record(self):
        '''Save the PlanRunRecord. Called at the end of the run. Other classes can also call
        this method to save the record during the plan run.
        '''
        if len(self.run_record.__dict__) > 0:
            serialize.save(self.run_record, self.output_dir_path / PLAN_RUN_RECORD_FILENAME)

    def calc_total_progress_steps(self):
        self.total_progress_steps += len(self.bible_ranges) * len(self.all_versions)
        
        for bible_version in self._all_versions.keys():
            if bible_version.auto_font:
                self.total_progress_steps += 1

        for output in multiscript.app().outputs_for_ext(self.base_template_path.suffix):
            try:
                self.total_progress_steps += output.get_total_progress_steps(self)
            except Exception as exception:
                _logger.debug(f"The output {output.name} raised an exception:")
                _logger.exception(exception)

    def load_bible_content(self):
        all_sources = set()
        for version in self.all_versions:
            all_sources.add(version.bible_source)
        for source in all_sources:
            try:
                source.bible_content_loading(self)
            except Exception as exception:
                _logger.debug(f"The source {source.name} raised an exception:")
                _logger.exception(exception)

        _logger.info("Loading Bible versions:")

        try:
            for version in self.all_versions:
                _logger.info(f"\tLoading {version.abbrev}:")
                content_list = []

                for bible_range in self.bible_ranges:
                    content = BibleContent()
                    content.bible_version = version
                    content.bible_range = bible_range
                    _logger.info(f"\t\tLoading {str(bible_range)}")
                    self.monitors.set_substatus_text(f"Loading {version.abbrev} {str(bible_range)}")
                    try:
                        version.load_content(bible_range, content, self)
                    except Exception as exception:
                        _logger.exception(exception)
                        self.monitors.request_confirmation(f"<b>There was an error loading {str(bible_range)} " +
                                                        f"for the {version.abbrev}.</b>")
                    content_list.append(content)
                    
                    # Noe: self.increment_progress_step_count() allows cancellation, which means a CancelError
                    # can be raised during this call.
                    self.increment_progress_step_count()

                self.bible_contents[version] = content_list
        finally:
            # Allow sources to clean up after themselves, even if we had an unhandled exception, which could
            # include a CancelError.
            for source in all_sources:
                try:
                    source.bible_content_loaded(self)
                except Exception as exception:
                    _logger.debug(f"The source {source.name} raised an exception:")
                    _logger.exception(exception)

    def select_auto_fonts(self):
        _logger.info("Selecting fonts:")

        ignored_scripts_str = multiscript.app().app_config_group.general.ignored_scripts
        ignored_scripts = {string.strip() for string in ignored_scripts_str.split(',')}

        for bible_version in self._all_versions.keys():
            if bible_version.auto_font:
                bible_text = ""
                for bible_contents in self.bible_contents[bible_version]:
                    bible_text += bible_contents.body.all_text()
                
                text_info = self.font_finder.analyse(bible_text)
                script_display = text_info.main_script
                if text_info.script_variant != "":
                    script_display += f" ({text_info.script_variant})"

                if text_info.main_script in ignored_scripts:
                    _logger.info(f"\tFont family not selected for {script_display} script in {bible_version.abbrev}.")
                else:
                    font_family = self.font_finder.find_family(text_info)
                    bible_version.font_family = font_family
                    bible_version.auto_font = False
                    self.plan.changed = True
                    _logger.info(f"\tSelected {font_family} for {script_display} script in {bible_version.abbrev}.")
                
                self.increment_progress_step_count()

    def download_and_install_fonts(self):
        try:
            font_families = [bible_version.font_family for bible_version in self._all_versions.keys() if \
                             bible_version.font_family is not None and bible_version.font_family != ""]
            _logger.info("Checking installed fonts...")
            if len(self.font_finder.not_installed_families(font_families)) == 0:
                _logger.info("All font families already installed.")
                return
            
            fonts_for_download = self.font_finder.find_family_fonts_to_download(font_families)
            if len(fonts_for_download) == 0:
                _logger.info("No fonts available for download.")
                return
            if not multiscript.app().app_config_group.general.download_and_install_fonts:
                _logger.info("Settings don't allow font download.")
                return
            
            self.total_progress_steps += len(fonts_for_download) + 1 # One step per download + one for install
            self.update_progress()
            # print(fonts_for_download)
            families_for_download = {font_info.family_name: 1 for font_info in fonts_for_download}.keys()                    
            _logger.info("Preparing to download these font families:")
            for font_family in families_for_download:
                _logger.info(f"\t{font_family}")    
            self.monitors.request_confirmation("Press <b>Continue</b> to download and install fonts for " +
                                                "this plan...")
            
            _logger.info("Dowloading fonts:")
            # Need a temporary directory from here.
            # Download fonts
            fonts_for_install = []
            font_total_count = len(fonts_for_download)
            for font_index in range(font_total_count):
                # We make a copy so as not to affect the original FontInfo object
                font_info = fonts_for_download[font_index].copy()
                _logger.info(f"\tDownloading {font_info.filename}")
                response = requests.get(font_info.url, stream=True)
                font_info.downloaded_path = self.temp_dir_path / font_info.filename
                bytes_written = 0
                with open(font_info.downloaded_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=128):
                        bytes_written += file.write(chunk)
                        kb_written = int(bytes_written / 1024) 
                        self.monitors.set_substatus_text(
                            f"Downloading {font_info.fullname} (font file {font_index+1} of {font_total_count} - " +
                            f"{kb_written}K)...")
                        self.monitors.allow_cancel()
                fonts_for_install.append(font_info)
                self.increment_progress_step_count()
            # End need of temporary directory

                # Install fonts
                _logger.info("Installing fonts...")
                self.font_finder.install_fonts(fonts_for_install)
                self.increment_progress_step_count()
                                                            
        except fontfinder.UnsupportedPlatformException:
            _logger.info(f"Font download and installation not currently supported on this platform.")

    def create_bible_outputs(self):
        _logger.info("Creating outputs:")

        for output in multiscript.app().outputs_for_ext(self.base_template_path.suffix):
            _logger.info("\tCreating " + output.name + " output:")
            try:
                output.generate_all(self)
            except Exception as exception:
                _logger.exception(exception)
                self.monitors.request_confirmation(f"<b>There was an error creating the {output.name} output.</b>")

    def increment_progress_step_count(self):
        self.progress_step_count += 1
        self.update_progress()
        self.monitors.allow_cancel()

    def update_progress(self):
        self.monitors.set_progress_percent(int(self.progress_step_count / self.total_progress_steps * 100))


class PlanRunRecord:
    '''Class for holding data from a plan run that needs to be persisted in the output directory (e.g. cache
    data). Objects called by the PlanRunner may persist data by adding attributes to instances of this class.
    '''
    pass


class CancelError(MultiscriptException):
    def __init__(self):
        pass


