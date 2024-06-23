
from dataclasses import dataclass
import logging
from pathlib import Path
import shutil

from multiscript.outputs.base import BibleOutput
from multiscript.plan.runner import PlanRunner
from multiscript.plan.symbols import column_symbols
from multiscript.util import compare


_logger = logging.getLogger(__name__)


class FileSetOutput(BibleOutput):
    '''An abstract BibleOutput that produces a set of files. Each output item is a separate file.
    Create a subclass for each individual file type.

    When a file is loaded into memory, this class refers to it as a document.

    Subclasses should override __init__(), load_document(), save_document(), and
    fill_bible_content(). Subclasses can optionally override expand_base_template(),
    begin_fill_document(), end_fill_document(), and if necessary override the algorithm
    in fill_bible_content().
    '''
    def __init__(self, plugin):
        '''Subclasses should override this method to set self.file_ext to the appropriate file
        extension.
        '''
        super().__init__(plugin)
        self.output_file_ext: str = "" # e.g. ".output"

    def setup(self, runner):
        '''Overriden from BibleOutput.setup(). Called prior to looping through the version
        combos.

        We use this method to set up the cache of file metadata for the run.
        '''
        super().setup(runner)
        empty_file_metadata: dict[str, 'FileMetaData'] = {}
        try:
            # Check if the existing plan run record has a metadata cache
            fileset_metadata = runner.run_record.fileset_metadata
        except AttributeError:
            # If not, create a blank cache.
            runner.run_record.fileset_metadata = empty_file_metadata

    def cache_file_metadata(self, runner, path):
        '''Get the on-disk metatdata for the given path, and store it in the cache'''
        runner.run_record.fileset_metadata[str(path)] = FileMetaData(path)

    def get_cached_file_metadata(self, runner, path):
        '''Returns the cached FileMetaData for the given path, or None if no metadata in the cache.'''
        return runner.run_record.fileset_metadata.get(str(path), None)

    def cleanup(self, runner):
        '''Overriden from BibleOutput.cleanup(). Called after looping through the version
        combos.

        We use this method to save up the cache of file metadata for the run.
        '''
        super().cleanup(runner)
        self.prune_file_metadata(runner)
        runner.save_plan_run_record()

    def prune_file_metadata(self, runner):
        for str_path in list(runner.run_record.fileset_metadata.keys()):
            if not Path(str_path).exists():
                del runner.run_record.fileset_metadata[str_path]

    def generate_combo_item(self, runner, version_combo, template_obj=None, is_template=False):
        '''Overrides BibleOutput.generate_combo_item(). The item returned is the path
        to the file generated.

        Subclasses don't need to override this method, but instead override load_document(),
        save_document(), and fill_bible_content(). Subclasses can optionally override
        expand_base_template(), begin_fill_document(), end_fill_document(), and if necessary
        override the algorithm in fill_document().
        '''
        filepath = self.get_item_filepath(runner, version_combo, is_template)

        # We normally save to the expected filepath, unless we need to check if the output has really changed,
        # in which case we will save to a temporary directory.
        savepath = filepath
        if filepath.exists() and not runner.plan.config.general.always_overwrite_output:
            keep_existing_file = False
            cached_metadata = self.get_cached_file_metadata(runner, filepath)
            if cached_metadata is not None:
                if cached_metadata != FileMetaData(filepath):
                    # Existing file has been edited. Don't overwrite it.
                    keep_existing_file = True
            else:
                # We have no metadata for the file. For safety, assume it has been edited.
                keep_existing_file = True
            
            if keep_existing_file:
                self.log_keep_edited_file(runner, filepath, is_template)
                return filepath
            else:
                # We will create the output in a temporary directory first, so we can compare it to the existing file
                # and determine whether it even needs replacing.
                savepath = runner.temp_dir_path / filepath.name

        self.log_preparing_file(runner, filepath, is_template)
        template_path = Path(template_obj)
        document = self.load_document(runner, version_combo, template_path)
        
        is_base_template_and_edited = False
        if template_obj == runner.base_template_path:
            self.expand_base_template(runner, document)
            if runner.plan.config.general.confirm_after_template_expansion:
                self.save_document(runner, version_combo, document, savepath)
                self.cache_file_metadata(runner, savepath)
                runner.monitors.request_confirmation(
                    "<b>Open</b> and check the expanded template, then click <b>Continue</b> " +
                    "once you have saved any changes.",
                    savepath)
                if self.get_cached_file_metadata(runner, savepath) != FileMetaData(savepath):
                    # Template was edited, so reload from disk.
                    is_base_template_and_edited = True
                    document = self.load_document(runner, version_combo, savepath)

        self.begin_fill_document(runner, version_combo, document, is_template)
        self.fill_document(runner, version_combo, document, is_template)
        self.end_fill_document(runner, version_combo, document, is_template)
        self.save_document(runner, version_combo, document, savepath)

        if savepath != filepath:
            if compare.cmp_file(savepath, filepath, expand_zip=True):
                # New file is identical to the existing file, so no need to update the existing file.
                self.log_file_unchanged(runner, filepath, is_template)
                return filepath
            else:
                # Replace existing file with new file.
                shutil.copy2(savepath, filepath)
                _logger.debug(f'Copied "{savepath}" to "{filepath}"')
        self.log_file_created(runner, filepath, is_template)
        if is_base_template_and_edited:
            # We don't want to update the cached metadata, so that the saved template will show as edited
            # on the next run through.
            pass
        else:
            self.cache_file_metadata(runner, filepath)

        if is_template:
            runner.monitors.request_confirmation(
                "<b>Open</b> and check the template, then click <b>Continue</b> once you have saved any changes.",
                filepath)

        return filepath
    
    def fill_document(self, runner, version_combo, document, is_template):
        for element in version_combo:
            symbol_index = element.version_column.symbol_index
            column_symbol = column_symbols[symbol_index]
            version = element.version
            if version is None and is_template:
                # No need to fill in Bible content, so skip this version
                continue

            if version is not None:
                bible_content_count = len(runner.bible_contents[version])
            else:
                # Just count Bible content for the first version
                if len(runner.bible_contents.values()) > 0:
                    bible_content_count = len(list(runner.bible_contents.values())[0])
                else:
                    bible_content_count = 0

            for contents_index in range(bible_content_count):
                if version is not None:
                    bible_content = runner.bible_contents[version][contents_index]
                    _logger.info(f"\t\t\tFilling passage {str(contents_index+1)}{column_symbol} with " +
                                f"{str(bible_content.bible_version.abbrev)} {str(bible_content.bible_range)}")
                else:
                    bible_content = None
                    # _logger.info(f"\t\t\tLeaving passage {str(contents_index+1)}{column_symbol} blank.")
                self.fill_bible_content(runner, document, contents_index, column_symbol, bible_content)

    def log_keep_edited_file(self, runner, filepath, is_template):
        log_message = f"\t\tKeeping edited {'template' if is_template else 'output'} {filepath.name}"
        runner.monitors.set_substatus_text(log_message.strip())
        _logger.info(log_message)

    def log_preparing_file(self, runner, filepath, is_template):
        log_message = f"\t\tPreparing {'template ' if is_template else ''}{filepath.name}"
        runner.monitors.set_substatus_text(log_message.strip())
        _logger.info(log_message)

    def log_file_unchanged(self, runner, filepath, is_template):
        log_message = f"\t\t\tNo changes to {'template' if is_template else 'file'}."
        runner.monitors.set_substatus_text(log_message.strip())
        _logger.info(log_message)

    def log_file_created(self, runner, filepath, is_template):
        log_message = f"\t\t\tSaved {'template' if is_template else 'file'}."
        runner.monitors.set_substatus_text(log_message.strip())
        _logger.info(log_message)

    def get_item_filepath(self, runner, version_combo, is_template):
        return runner.output_dir_path / Path(self.get_item_filename(runner, version_combo, is_template))

    def get_item_filename(self, runner, version_combo, is_template):
        filename = self.get_item_stem(runner, version_combo)
        filename += ("_template" if is_template else "") + self.output_file_ext
        return filename
    
    def get_item_stem(self, runner: PlanRunner, version_combo):
        item_name = runner.bible_ranges[0].str(abbrev=True, alt_sep=True, nospace=True)

        if len(runner.bible_ranges) > 1:
            item_name += " +" + str(len(runner.bible_ranges)-1)

        item_name += " "
        version_combo.sort_by_col_symbol()
        version_names = []
        for element in version_combo:
            version = element.version
            if version is None:
                version_names.append("-")
            else:
                version_name = version.user_labels.lang + "-" + version.user_labels.abbrev
                version_names.append(version_name)
        item_name += ",".join(version_names)
        
        return item_name

    def load_document(self, runner, version_combo, template_path):
        '''Subclasses must override this method to returns a document representation of the
        template at template_path, suitable for expansion and filling with content,
        to later be saved as a new file. The document object itself is opaque to FileSetOuput.
        '''
        return object()
    
    def save_document(self, runner, version_combo, document, filepath):
        '''Subclasses must override this method to save the document as a new file.
        The document object itself is opaque to FileSetOuput.
        '''
        pass

    def expand_base_template(self, runner, document):
        '''Called if the newly loaded document is actually the base template. Subclasses
        can override this method if they want to expand any tags in the base template
        that don't depend on the current version_combo.
        '''
        pass

    def begin_fill_document(self, runner, version_combo, document, is_template):
        '''Called immediately before fill_document(). Subclasses can override to
        perform any tasks that should be completed before BibleContents are inserted
        into the document.
        '''
        pass

    def fill_bible_content(self, runner, document, contents_index, column_symbol, bible_content):
        '''Subclasses must override this method to insert the specified bible_content into the document,
        at the specified contents_index and column_symbol.
        '''
        pass

    def end_fill_document(self, runner, version_combo, document, is_template):
        '''Called immediately after fill_document(). Subclasses can override to
        perform any tasks that should be completed after BibleContents have been inserted
        into the document.
        '''
        pass


@dataclass
class FileMetaData:
    size:   int     # Size in bytes
    mtime:  float   # Modification time in seconds

    def __init__(self, pathlike=None):
        if pathlike is not None:
            stat_result = Path(pathlike).stat()
        self.size = stat_result.st_size if pathlike is not None else 0
        self.mtime = stat_result.st_mtime if pathlike is not None else 0
