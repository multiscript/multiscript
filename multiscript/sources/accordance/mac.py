
from pathlib import Path

import applescript

from multiscript.sources.base import BibleSource
from multiscript.sources.accordance import AccordancePlatform


class AccordanceMacPlatform(AccordancePlatform):
    def __init__(self, bible_source: BibleSource):
        super().__init__(bible_source)

        self.DEFAULT_ACCORDANCE_DATA_PATH = "~/Library/Application Support/Accordance"
        self.DEFAULT_MOD_NAME_DB_PATH = "/Applications/Accordance.app/Contents/Resources/modNameDB.strings"

        script_lib_path = Path(__file__, "../accordance.applescript").resolve()
        self.script_lib = applescript.AppleScript(path=str(script_lib_path))

    def load_module_ui_names(self):
        '''Returns the list of Accordance text modules as displayed in the Get Verses dialog.'''
        return [str(name) for name in self.script_lib.call("get_module_ui_names")]
    
    def get_bible_text(self, accordance_module_id: str, bible_range_str: str):
        bible_text = self.script_lib.call("get_text_via_api", accordance_module_id, bible_range_str, False)
        return bible_text
