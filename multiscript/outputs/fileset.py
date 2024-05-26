
from dataclasses import dataclass
import logging
import os
from pathlib import Path
from typing import Any

import multiscript
from multiscript.outputs.base import BibleOutput
from multiscript.plan.runner import PlanRunner
from multiscript.plan.symbols import column_symbols
from multiscript.util import serialize


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
        file_metadata: dict[str, 'FileMetaData'] = {}
        runner.fileset_metadata = file_metadata

    def cleanup(self, runner):
        '''Overriden from BibleOutput.cleanup(). Called after looping through the version
        combos.

        We use this method to save up the cache of file metadata for the run.
        '''
        super().cleanup(runner)
        serialize.save(runner.fileset_metadata, runner.output_dir_path / "_metadata.json")

    def generate_combo_item(self, runner, version_combo, template_obj=None, is_template=False):
        '''Overrides BibleOutput.generate_combo_item(). The item returned is the path
        to the file generated.

        Subclasses don't need to override this method, but instead override load_document(),
        save_document(), and fill_bible_content(). Subclasses can optionally override
        expand_base_template(), begin_fill_document(), end_fill_document(), and if necessary
        override the algorithm in fill_bible_content().
        '''
        filepath = self.get_item_filepath(runner, version_combo, is_template)

        if (multiscript.app().app_config_group.general.keep_existing_template_files and \
            is_template and filepath.exists()) or \
           (multiscript.app().app_config_group.general.keep_existing_output_files and \
            not is_template and filepath.exists()):
            self.log_keep_existing_filepath(runner, filepath, is_template)
            return filepath

        self.log_combo_item(runner, version_combo, is_template)
        
        template_path = Path(template_obj)
        document = self.load_document(runner, version_combo, template_path)
        
        if template_obj == runner.base_template_path:
            self.expand_base_template(runner, document)
            if runner.plan.config.general.confirm_after_template_expansion:
                self.save_document(runner, version_combo, document, filepath)
                runner.monitors.request_confirmation(
                    "<b>Open</b> and check the expanded template, then click <b>Continue</b> " +
                    "once you have saved any changes.",
                    filepath)
        
        self.begin_fill_document(runner, version_combo, document, is_template)
        self.fill_document(runner, version_combo, document, is_template)
        self.end_fill_document(runner, version_combo, document, is_template)

        self.save_document(runner, version_combo, document, filepath)
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
                    # _logger.info(f"\t\t\tLeaving passage {str(contents_index+1)}{column_symbol} blank.")
                    bible_content = None
                self.fill_bible_content(runner, document, contents_index, column_symbol, bible_content)

    def log_keep_existing_filepath(self, runner, filepath, is_template):
        log_message = f"Keeping existing {'template' if is_template else 'output'} {filepath.name}"
        runner.monitors.set_substatus_text(log_message)
        _logger.info("\t\t" + log_message)

    def log_combo_item(self, runner, version_combo, is_template):
        filename = self.get_item_filename(runner, version_combo, is_template)
        log_message = f"Creating {'template ' if is_template else ''}{filename}"
        runner.monitors.set_substatus_text(log_message)
        _logger.info("\t\t" + log_message)

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
        Before loading the document, subclasses should call super().load_document().
        '''
        return object()
    
    def save_document(self, runner, version_combo, document, filepath):
        '''Subclasses must override this method to save the document as a new file.
        The document object itself is opaque to FileSetOuput.
        After saving the document, subclasses should call super().save_document().
        '''
        runner.fileset_metadata[str(filepath)] = FileMetaData(filepath)

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
        else:
            stat_result = os.stat_result()
        self.size = stat_result.st_size
        self.mtime = stat_result.st_mtime