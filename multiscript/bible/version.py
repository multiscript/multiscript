
from pprint import pformat

import multiscript


class BibleVersion:
    '''Class to hold information about a particular Bible version from a particular
    BibleSource.
    '''
    def __init__(self, source=None, id=None, name=None, lang=None, abbrev=None):
        self.bible_source = source
        self.id = id
        self.user_labels = BibleVersionLabels()
        self.native_labels = BibleVersionLabels()
        self.name = name                    # Shortcut to set user version name
        self.lang = lang                    # Shortcut to set user version lang
        self.abbrev = abbrev                # Shortcut to set user version abbrev
        self.notes = ""                     # String data of version notes
        self.notes_type = "text/markdown"   # Media-type of plan notes. Currently only "text/markdown" supported.
        self.output_config = {}             # Dict of OutputVersionConfig by output long_id

        for output in multiscript.app().all_outputs:
            output_version_config = output.new_output_version_config()
            if output_version_config is not None:
                self.output_config[output.long_id] = output_version_config

    @property
    def long_id(self):
        '''Returns the long id of this object, which for a BibleVersion is a combination of its
        BibleSource long_id and the BibleVersion's (short) id.'''
        return self.bible_source.long_id + "/" + self.id

    # Returns combined native and user version name
    @property
    def name(self):
        if self.user_labels.name is None or self.user_labels.name == "":
            return self.native_labels.name
        if self.native_labels.name is None or self.native_labels.name == "":
            return self.user_labels.name
        return f"{self.native_labels.name} ({self.user_labels.name})"

    # Shortcut for setting user version name
    @name.setter
    def name(self, value):
        self.user_labels.name = value if value is not None else ""

    # Returns combined native and user version lang
    @property
    def lang(self):
        if self.user_labels.lang is None or self.user_labels.lang == "":
            return self.native_labels.lang
        if self.native_labels.lang is None or self.native_labels.lang == "":
            return self.user_labels.lang
        return f"{self.native_labels.lang} ({self.user_labels.lang})"

    # Shortcut for setting user version lang
    @lang.setter
    def lang(self, value):
        self.user_labels.lang = value if value is not None else ""

    # Returns combined native and user version abbrev
    @property
    def abbrev(self):
        if self.user_labels.abbrev is None or self.user_labels.abbrev == "":
            return self.native_labels.abbrev
        if self.native_labels.abbrev is None or self.native_labels.abbrev == "":
            return self.user_labels.abbrev
        return f"{self.native_labels.abbrev} ({self.user_labels.abbrev})"

    # Shortcut for setting user version abbrev
    @abbrev.setter
    def abbrev(self, value):
        self.user_labels.abbrev = value if value is not None else ""

    def load_content(self, bible_range, bible_content):
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
