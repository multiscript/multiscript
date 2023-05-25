from enum import Enum, auto

from bibleref.ref import BibleBook, BibleVerse, BibleRange
from bible.version import BibleVersion

PART_NAME_LEN_WIDTH   = 25 # For justifying string representations of BibleContentParts


class BibleContent:
    def __init__(self):
        self._bible_range: BibleRange = None
        self.bible_version: BibleVersion = None
        self.body: BibleStream = BibleStream(self)
        self.copyright_text: str = ""

    @property
    def bible_range(self) -> BibleRange:
        return self._bible_range
    
    @bible_range.setter
    def bible_range(self, value: BibleRange):
        self._bible_range: BibleRange = value
        self.body.current_verse = self._bible_range.start

    def __str__(self):
        string = ""
        if self.bible_version is not None:
            string = "Source: " + str(self.bible_version.bible_source.name) + "\n"
            string += "Version: " + str(self.bible_version.name) + "\n"
        string += "Range: " + str(self.bible_range) + "\n"
        string += str(self.body)
        string += "\nCopyright: " + self.copyright_text + "\n"
        return string


class BibleStreamHandler:
    def add_text(self, text):
        pass

    def add_start_paragraph(self, is_poetry=False):
        pass

    def add_end_paragraph(self):
        pass

    def add_line_break(self):
        pass

    def add_start_chap_num(self):
        pass

    def add_end_chap_num(self):
        pass

    def add_start_verse_num(self):
        pass

    def add_end_verse_num(self):
        pass

    def add_start_small_caps(self):
        pass

    def add_end_small_caps(self):
        pass


class BibleStream(BibleStreamHandler):
    def __init__(self, bible_content=None):
        self.bible_content: BibleContent = bible_content
        self.tokens: list[BibleStreamToken] = []
        self.current_verse: BibleVerse = None
        
        self.in_chap_num: bool = False
        self.in_verse_num: bool = False
        self.small_caps_level: int = 0

        #
        # Switches for various behavioural features
        #
        self.strip_text = False                     # If True, leading and trailing whitespace will be stripped
                                                    # before adding. If True, it's probably also wise to set
                                                    # self.insert_missing_whitespace to True, in order to add back
                                                    # in the minimum amount of needed whitespace.

        self.insert_missing_whitespace = False      # If True, whitespace will be added between strings if it
                                                    # doesn't exist.
        self.space_str = " "                        # Whitespace to add
 
        self.insert_missing_chap_num = False        # If True, a verse 1 without a previous chapter number will have
                                                    # the chapter number automatically inserted.
        self.insert_missing_first_verse_num = False # If True, a chapter number without a subsequent verse 1 number
                                                    # will have a verse 1 number automatically inserted.
        self.verse_sep = ":"                        # Verse separator use use between the chapter num and verse 1
                                                    # text.
        self.psalms_include_titles = True           # True if Psalms include titles, which are treated as part of
                                                    # verse 1 but occur before the verse 1 number.
        
        # TODO: Add switch to insert new paragraph at chapter boundaries if not provided.

        #
        # Internal flags and controls
        #
        self._expected_token_type = None            # Internal: if not None, the type of the token we're expecting next
        self._insert_space_before_text = False      # Internal flag: if True, whitespace will be added before
                                                    # the next text string.

    def constrain(self, bible_range):
        new_tokens = []
        for token in self.tokens:
            if bible_range.contains(token.bible_verse):
                new_tokens.append(token)
        self.tokens = new_tokens
        #
        # TODO: Close any unbalanced tokens. (e.g. we may have truncated a paragraph part-way through, so it would
        # be good to add any missing close-paragraph or open-paragraph tokens etc.)
        #

    def copyStreamTo(self, bible_stream_handler):
        for token in self.tokens:
            token.copyTokenTo(bible_stream_handler)

    def add_token(self, token):
        if self._expected_token_type is not None and token.type is not self._expected_token_type:
            self.handle_unexpected_token(token)
        
        token.bible_verse = self.current_verse
        self.tokens.append(token)

    def handle_unexpected_token(self, token):
        # We already know the token is not of the expected type.
        
        # If necessary, add any missing verse 1 number.
        if self.insert_missing_first_verse_num and \
            self._expected_token_type is BibleStreamTokenType.START_VERSE_NUM:
            # If our range is a Psalm, and Psalms contain titles, we don't need to insert the
            # verse number. So only proceed if those conditions *don't* hold.
            bible_range = self.bible_content.bible_range
            if bible_range is None or bible_range.book is not BibleBook.Psa or not self.psalms_include_titles:
                self._expected_token_type = None # Prevents infinite recursion
                self._insert_space_before_text = False   # We don't want extra space here
                self.add_start_verse_num()
                self.add_text(self.verse_sep + "1")
                self.add_end_verse_num()

    def add_text(self, text):
        if self.strip_text:
            text = text.strip()

        if self.insert_missing_whitespace and self._insert_space_before_text and \
            len(text) > 0 and not text[0].isspace():                
            text = self.space_str + text
        
        if len(text) > 0:
            self.add_token(BibleTextToken(self, self.current_verse, text))        
            if self.insert_missing_whitespace:
                self._insert_space_before_text = not text[-1].isspace()

    def add_start_paragraph(self, is_poetry=False):
        self.add_token(BibleStartParagraphToken(self, self.current_verse, is_poetry))
        self._insert_space_before_text = False # First text of para needs no leading space

    def add_end_paragraph(self):
        self.add_token(BibleEndParagraphToken(self, self.current_verse))

    def add_line_break(self):
        self.add_token(BibleLineBreakToken(self, self.current_verse))
        self._insert_space_before_text = False # First text of new line needs no leading space

    def add_start_chap_num(self):
        # If a space is needed, insert it now before the start of the chapter number
        self._insert_any_needed_space_before_number()
        self.add_token(BibleStartChapNumToken(self, self.current_verse))
        self.in_chap_num = True

    def add_end_chap_num(self):
        self.add_token(BibleEndChapNumToken(self, self.current_verse))
        self.in_chap_num = False
        if self.insert_missing_first_verse_num:
            self._expected_token_type = BibleStreamTokenType.START_VERSE_NUM

    def add_start_verse_num(self):
        # If a space is needed, insert it now before the start of the verse number
        self._insert_any_needed_space_before_number()

        # If necessary, add any missing chap number
        if self.insert_missing_chap_num and \
           self.current_verse is not None and self.current_verse == self.current_verse.first_verse() and \
           (len(self.tokens) == 0 or self.tokens[-1].type is not BibleStreamTokenType.END_CHAP_NUM):
            
            self.add_start_chap_num()
            self.add_text(str(self.current_verse.chap_num))
            self.add_end_chap_num()
            self.add_token(BibleStartVerseNumToken(self, self.current_verse))
            self._insert_space_before_text = False  # We don't want extra space here
            self.add_text(self.verse_sep)   # We need to add the verse seperator inside the verse num section
            self._insert_space_before_text = False  # We don't want extra space here
        else:
            self.add_token(BibleStartVerseNumToken(self, self.current_verse))
        self.in_verse_num = True

    def add_end_verse_num(self):
        self.add_token(BibleEndVerseNumToken(self, self.current_verse))
        self.in_verse_num = False

    def add_start_small_caps(self):
        self.add_token(BibleStartSmallCapsToken(self, self.current_verse))
        self.small_caps_level += 1

    def add_end_small_caps(self):
        self.add_token(BibleEndSmallCapsToken(self, self.current_verse))
        self.small_caps_level -= 1

    def _insert_any_needed_space_before_number(self):
        if self.insert_missing_whitespace and self._insert_space_before_text:
            # Stripping text needs to be turned off in order to add a string that
            # is only space. So we need to save and restore the state of self.strip_text
            strip_text = self.strip_text
            self.strip_text = False
            self.add_text(self.space_str)
            self.strip_text = strip_text

            # For the text we just added, use the verse metadata of the previous token.
            if len(self.tokens) > 1:
                self.tokens[-1].bible_verse = BibleVerse(self.tokens[-2].bible_verse)

    def __str__(self):
        string = ""
        for part in self.tokens:
            string += str(part) + "\n"
        return string[:-1] # Remove trailing newline


class BibleStreamTokenType(Enum):
    ''' This Enum allows the type of a BibleStreamToken to be determined faster than
    calling isinstance()
    '''
    TEXT                = auto()
    START_PARA          = auto()
    END_PARA            = auto()
    LINE_BREAK          = auto()
    START_CHAP_NUM      = auto()
    END_CHAP_NUM        = auto()
    START_VERSE_NUM     = auto()
    END_VERSE_NUM       = auto()
    START_SMALL_CAPS    = auto()
    END_SMALL_CAPS      = auto()


class BibleStreamToken:
    def __init__(self, bible_stream, bible_verse):
        self.bible_stream: BibleStream = bible_stream
        self.bible_verse: BibleVerse = bible_verse
        self.type: BibleStreamTokenType = None # For testing the type of the token faster than calling isinstance()
        self.is_start: bool = False   # True for tokens that represent the start of something
        self.is_end: bool = False     # True for tokens that represent the end of something
        self.has_text: bool = False   # True for tokens that contain text

    def copyTokenTo(self, bible_stream_handler):
        '''Subclasses to override.
        '''
        pass

    def __str__(self):
        string = ""
        if self.bible_verse is not None:
            string += self.bible_verse.str(abbrev=True) + " "
        string += self._token_name_for_str().ljust(PART_NAME_LEN_WIDTH) + "|"
        return string

    def _token_name_for_str(self):
        token_name = type(self).__name__
        token_name = token_name.replace("Bible","")
        token_name = token_name.replace("Token","")
        return token_name


class BibleTextToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse, text):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.TEXT
        self.has_text = True
        self.text = text

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_text(self.text)

    def __str__(self):
        return super().__str__() + self.text + "|"


class BibleStartParagraphToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse, is_poetry=False):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.START_PARA
        self.is_start = True
        self.is_poetry = is_poetry

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_start_paragraph(self.is_poetry)

    def _token_name_for_str(self):
        token_name = super()._token_name_for_str()
        token_name += " (Poetry)" if self.is_poetry else ""
        return token_name     


class BibleEndParagraphToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.END_PARA
        self.is_end = True

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_end_paragraph()


class BibleLineBreakToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.LINE_BREAK

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_line_break()


class BibleStartChapNumToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.START_CHAP_NUM
        self.is_start = True

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_start_chap_num()


class BibleEndChapNumToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.END_CHAP_NUM
        self.is_end = True

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_end_chap_num()


class BibleStartVerseNumToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.START_VERSE_NUM
        self.is_start = True

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_start_verse_num()


class BibleEndVerseNumToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.END_VERSE_NUM
        self.is_end = True

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_end_verse_num()


class BibleStartSmallCapsToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.START_SMALL_CAPS
        self.is_start = True

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_start_small_caps()


class BibleEndSmallCapsToken(BibleStreamToken):
    def __init__(self, bible_stream, bible_verse):
        super().__init__(bible_stream, bible_verse)
        self.type = BibleStreamTokenType.END_SMALL_CAPS
        self.is_end = True

    def copyTokenTo(self, bible_stream_handler):
        bible_stream_handler.add_end_small_caps()

