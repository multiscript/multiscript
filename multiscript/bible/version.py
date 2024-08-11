
import locale
from pprint import pformat

import langcodes

import multiscript


class BibleVersion:
    '''Class to hold information about a particular Bible version from a particular
    BibleSource.
    '''
    def __init__(self, source: 'BibleSource' = None, id: str = None, name: str = None, lang: str = None,
                 abbrev: str = None):
        self.bible_source: 'BibleSource' = source
        self.id: str = id
        self.user_labels: BibleVersionLabels = BibleVersionLabels()
        self.native_labels: BibleVersionLabels = BibleVersionLabels()
        self.name = name                        # Shortcut to set user version name
        self.lang = lang                        # Shortcut to set user version lang
        self.abbrev = abbrev                    # Shortcut to set user version abbrev
        self.notes: str = ""                    # String data of version notes
        self.notes_type: str = "text/markdown"  # Media-type of plan notes. Currently only "text/markdown" supported.
        self.copyright: str = ""                # String data of copyright text
        self.copyright_type: str = "text/plain" # Media-type of copyright text. Currently only "text/plain" supported
        self.auto_font: bool = True             # True if the font-family should be auto chosen on next plan run
        self.font_family: str = ""              # Font-family to use for this version
        self.is_rtl: bool = False               # True if the version uses a right-to-left script

        # Dict of OutputVersionConfig by output long_id
        self.output_config: dict[str, 'OutputVersionConfig'] = {}

        for output in multiscript.app().all_outputs:
            output_version_config = output.new_output_version_config()
            if output_version_config is not None:
                self.output_config[output.long_id] = output_version_config

    @property
    def long_id(self) -> str:
        '''Returns the long id of this object, which for a BibleVersion is a combination of its
        BibleSource long_id and the BibleVersion's (short) id.'''
        return self.bible_source.long_id + "/" + self.id

    @property
    def name(self) -> str:
        '''Returns the combine native and user version names'''
        if self.user_labels.name is None or self.user_labels.name == "":
            return self.native_labels.name
        if self.native_labels.name is None or self.native_labels.name == "":
            return self.user_labels.name
        return f"{self.native_labels.name} ({self.user_labels.name})"

    @name.setter
    def name(self, value: str):
        '''Shortcut for the setting the user version name'''
        self.user_labels.name = value if value is not None else ""

    @property
    def lang(self) -> str:
        '''Returns the combine native and user version language string (user-facing string, not a lang code)'''
        if self.user_labels.lang is None or self.user_labels.lang == "":
            return self.native_labels.lang
        if self.native_labels.lang is None or self.native_labels.lang == "":
            return self.user_labels.lang
        return f"{self.native_labels.lang} ({self.user_labels.lang})"

    # Shortcut for setting user version lang
    @lang.setter
    def lang(self, value: str):
        '''Shortcut for the setting the user version language string (user-facing string, not a lang code)'''
        self.user_labels.lang = value if value is not None else ""

    @property
    def abbrev(self) -> str:
        '''Returns the combine native and user version abbreviation string'''
        if self.user_labels.abbrev is None or self.user_labels.abbrev == "":
            return self.native_labels.abbrev
        if self.native_labels.abbrev is None or self.native_labels.abbrev == "":
            return self.user_labels.abbrev
        return f"{self.native_labels.abbrev} ({self.user_labels.abbrev})"

    @abbrev.setter
    def abbrev(self, value: str):
        '''Shortcut for the setting the user version abbreviation string'''
        self.user_labels.abbrev = value if value is not None else ""

    def set_lang_from_code(self, lang_code: str):
        '''Sets the user and native version languages string from an IETF language code'''
        vers_lang_obj = langcodes.Language.get(lang_code)
        user_locale = locale.getlocale()
        if user_locale is not None and len(user_locale) > 0:
            user_lang_code = user_locale[0]
        else:
            user_lang_code = 'en' # Use English if we can't determine local language
        self.user_labels.lang = vers_lang_obj.display_name(user_lang_code).capitalize()
        autonym = vers_lang_obj.autonym().capitalize()
        if autonym != self.user_labels.lang:
            self.native_labels.lang = autonym

    def load_content(self, bible_range, bible_content, plan_runner=None):
        pass        

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})" + "\n" + \
        pformat(self.__dict__)


class BibleVersionLabels:
    '''Class to hold display labels for a BibleVersion.
    '''
    def __init__(self, name=None, lang=None, abbrev=None):
        self.name = name if name is not None else ""
        self.lang = lang if lang is not None else ""
        self.abbrev = abbrev if abbrev is not None else ""

    def __repr__(self):
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)
