
import logging
from operator import attrgetter

import multiscript
from multiscript.bible.content import BibleContent
from multiscript.bible.reference import BibleRangeList
from multiscript.plan import combinations
from multiscript.plan.monitor import PlanMonitorCollection
from multiscript.util.exception import MultiscriptException

_logger = logging.getLogger(__name__)

class PlanRunner:
    '''This class oversees the process of running a Plan: reading the Bible passages from the sources,
    and writing the Bible passages to the outputs.
    '''
    def __init__(self, plan, monitor=None):
        self.plan = plan
        self.monitors = PlanMonitorCollection(self, monitor)
        self.total_progress_steps = 0
        self.progress_step_count = 0

        self.bible_ranges = []      # List of BibleRanges to be processed
        self._all_versions = {}     # Dict of all versions being used.
                                    #   Keys: versions Vals: True (we're using the dict as an ordered set)
        self.version_cols = []      # List of VersionColumns
        self.bible_contents = {}    # Uses BibleVersions as keys to a list of BibleContents (one
                                    #   one for each range in self.bible_ranges)
        self.output_runs = {}       # Dict of OutputPlanRun by output long_id

        #
        # Convert the data in the plan into the required form for this runner.
        #
        self.bible_ranges = BibleRangeList.new_from_text(plan.bible_passages)

        all_versions = plan.bible_versions
        for plan_version_column in plan.version_selection:
            column_version_list = []
            for row_index in range(len(plan_version_column)):
                if plan_version_column[row_index]:
                    column_version_list.append(all_versions[row_index])
            self._add_version_list(column_version_list)

        self.base_template_path = plan.template_path
        self.output_dir_path = plan.output_dir_path

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
    def all_versions(self):
        return self._all_versions.keys()

    @property
    def all_version_combos(self):
        return combinations.get_all_version_combos(self.version_cols)

    def run(self):
        self.calc_total_progress_steps()
        self.load_bible_content()
        self.create_bible_outputs()
        _logger.info("Finished")

    def calc_total_progress_steps(self):
        self.total_progress_steps += len(self.bible_ranges) * len(self.all_versions)
        
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
                    version.load_content(bible_range, content)
                except Exception as exception:
                    _logger.exception(exception)
                    self.monitors.request_confirmation(f"<b>There was an error loading {str(bible_range)} " +
                                                       f"for the {version.abbrev}.</b>")
                content_list.append(content)
                self.increment_progress_step_count()

            self.bible_contents[version] = content_list

        for source in all_sources:
            try:
                source.bible_content_loaded(self)
            except Exception as exception:
                _logger.debug(f"The source {source.name} raised an exception:")
                _logger.exception(exception)

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
        self.monitors.set_progress_percent(int(self.progress_step_count / self.total_progress_steps * 100))
        self.monitors.allow_cancel()


class CancelError(MultiscriptException):
    def __init__(self):
        pass


