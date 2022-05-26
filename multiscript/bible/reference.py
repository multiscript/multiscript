
import copy
from enum import Enum, auto

import scriptures

from multiscript.util.exception import MultiscriptException


# Internally, this module uses the scriptures module to perform conversion between
# bible references and strings. But this should not be relied upon. Only the public
# classes should be used: BibleBook, BibleVerse, BibleRange, BibleRangeList and the various
# error classes.

# TODO: Clarify how to validate extracting ranges from text.


class BibleBook(Enum):
    '''An enum for specifying books in the Bible.

    Note that Python identifiers can't start with a number. So books like
    1 Samuel are written here as _1Sam . The enum name (minus any _)
    becomes the book abbreviation, while the enum value becomes the full
    book title.
    '''
    Gen = "Genesis" 
    Exod = "Exodus"
    Lev = "Leviticus"
    Num = "Numbers"
    Deut = "Deuteronomy"
    Josh = "Joshua"
    Judg = "Judges"
    Ruth = "Ruth"
    _1Sam = "1 Samuel"
    _2Sam = "2 Samuel"
    _1Kgs = "1 Kings"
    _2Kgs = "2 Kings"
    _1Chr = "1 Chronicles"
    _2Chr = "2 Chronicles"
    Ezra = "Ezra"
    Neh = "Nehemiah"
    Esth = "Esther"
    Job = "Job"
    Psa = "Psalms"
    Prov = "Proverbs"
    Eccl = "Ecclesiastes"
    Song = "Song of Songs"
    Isa = "Isaiah"
    Jer = "Jeremiah"
    Lam = "Lamentations"
    Ezek = "Ezekiel"
    Dan = "Daniel"
    Hos = "Hosea"
    Joel = "Joel"
    Amos = "Amos"
    Obad = "Obadiah"
    Jonah = "Jonah"
    Mic = "Micah"
    Nah = "Nahum"
    Hab = "Habakkuk"
    Zeph = "Zephaniah"
    Hag = "Haggai"
    Zech = "Zechariah"
    Mal = "Malachi"
    Matt = "Matthew"
    Mark = "Mark"
    Luke = "Luke"
    John = "John"
    Acts = "Acts"
    Rom = "Romans"
    _1Cor = "1 Corinthians"
    _2Cor = "2 Corinthians"
    Gal = "Galatians"
    Eph = "Ephesians"
    Phil = "Philippians"
    Col = "Colossians"
    _1Thess = "1 Thessalonians"
    _2Thess = "2 Thessalonians"
    _1Tim = "1 Timothy"
    _2Tim = "2 Timothy"
    Titus = "Titus"
    Phlm = "Philemon"
    Heb = "Hebrews"
    James = "James"
    _1Pet = "1 Peter"
    _2Pet = "2 Peter"
    _1Jn = "1 John"
    _2Jn = "2 John"
    _3Jn = "3 John"
    Jude = "Jude"
    Rev = "Revelation"

    @property
    def abbrev(self):
        '''Abbreviated book name
        '''
        abbrev = self.name
        if abbrev[0] == "_":
            abbrev = abbrev[1:]
        return abbrev

    @property
    def title(self):
        '''Full book name
        '''
        return self.value


class BibleVerse:
    '''A reference to a single Bible verse. Contains 3 attributes:
    
    book  - The BibleBook enum of the book of the reference.
    chap  - The chapter number (indexed from 1) of the reference.
    verse - The verse number (indexed from 1) of the reference.
    '''
    def __init__(self, bible_book, chap_num, verse_num, validate=True):
        '''If validate is true, it checks that the reference is valid.
        If it's not valid, InvalidReferenceError is raised.
        '''
        if validate:
            try:
                ref_list = list(_scripture_text.normalize_reference(bible_book.abbrev, chap_num, verse_num))
            except scriptures.texts.base.InvalidReferenceException as e:
                raise InvalidReferenceError(f"{bible_book.abbrev} {chap_num}:{verse_num}") from e

            ref_list[0] = bible_book # Use the enum, rather than a string
        else:
            ref_list = (bible_book, chap_num, verse_num)
        
        self.book = ref_list[0]
        self.chap = ref_list[1]
        self.verse = ref_list[2]
       
    def __repr__(self):
        return str((self.book.abbrev, self.chap, self.verse))

    def __str__(self):
        return self.string()

    def string(self, abbrev=False, periods=False, nospace=False, nobook=False):
        '''Returns a string representation of this BibleVerse.

        If abbrev is True, the abbreviated name of the book is used (instead of the full name).
        If periods is True, chapter and verse numbers are separated by '.' instead of ':'.
        If nospace is True, no spaces are included in the string.
        If nobook is True, the book name is omitted.
        '''
        return _scripture_text.reference_to_string(self.book.abbrev, self.chap, self.verse, None, None,
                                                   abbrev, periods, nospace, nobook)

    def __eq__(self, other):
        return (self.book == other.book) and (self.chap == other.chap) and (self.verse == other.verse)

    def __lt__(self, other):
        if self.book != other.book:
            return NotImplemented
        else:
            return (self.chap < other.chap) or (self.chap == other.chap and self.verse < other.verse)

    def __le__(self, other):
        if self.book != other.book:
            return NotImplemented
        else:
            return (self.chap < other.chap) or (self.chap == other.chap and self.verse <= other.verse)

    def __gt__(self, other):
        if self.book != other.book:
            return NotImplemented
        else:
            return (self.chap > other.chap) or (self.chap == other.chap and self.verse > other.verse)

    def __ge__(self, other):
        if self.book != other.book:
            return NotImplemented
        else:
            return (self.chap > other.chap) or (self.chap == other.chap and self.verse >= other.verse)

    def copy(self):
        return copy.copy(self)

    def add(self, num_verses):
        ''' Return a new BibleVerse that is the specified number of verses after this verse.
        
        Returns None if the result would not be a valid reference in the book.
        '''
        new_chap = self.chap
        new_verse = self.verse + num_verses
        max_verse = self.max_verse(self.chap)
        while new_verse > max_verse:
            new_chap += 1
            if new_chap > self.max_chap():
                return None
            
            new_verse -= max_verse
            max_verse = self.max_verse(new_chap)

        return BibleVerse(self.book, new_chap, new_verse)

    def subtract(self, num_verses):
        ''' Return a new BibleVerse that is the specified number of verses before this verse.
        
        Returns None if the result would not be a valid reference in the book.
        '''
        new_chap = self.chap
        new_verse = self.verse - num_verses
        min_verse = self.min_verse(self.chap)
        while new_verse < min_verse:
            new_chap -= 1
            if new_chap < self.min_chap():
                return None
            
            new_verse += self.max_verse(new_chap)
            min_verse = self.min_verse(new_chap)

        return BibleVerse(self.book, new_chap, new_verse)

    def max_chap(self):
        '''Return highest chapter number (indexed from 1) of the book of this BibleVerse.
        '''
        return len(_info_by_book[self.book][3])

    def max_verse(self, chap=None):
        '''Return the highest verse number (indexed from 1) in the specified chapter
        of the book of this BibleVerse. If no chapter is specified, the chapter
        of this BibleVerse is used.
        '''
        if chap is None:
            chap = self.chap
        return _info_by_book[self.book][3][chap-1]

    def min_chap(self):
        '''Return lowest chapter number (indexed from 1) of the book of this BibleVerse.
        '''
        return 1

    def min_verse(self, chap=None):
        '''Return the lowest verse number (indexed from 1) in the specified chapter
        of the book of this BibleVerse. If no chapter is specified, the chapter
        of this BibleVerse is used.
        '''
        return 1


class BibleRange:
    '''A reference to a range of Bible verses. Contains 3 attributes:
    
    book  - The BibleBook enum of the book of the reference.
    start - The BibleVerse of the first verse in the range.
    end   - The BibleVerse of the last verse in the range.
    '''
    def __init__(self, bible_book, start_chap, start_verse=None, end_chap=None, end_verse=None, validate=True):
        self.book = bible_book
        self.start = BibleVerse(bible_book, start_chap, start_verse, validate=validate)
        self.end = BibleVerse(bible_book, end_chap, end_verse, validate=validate)

    def __eq__(self, other):
        return (self.book == other.book) and (self.start == other.start) and (self.end == other.end)

    def contains(self, bible_verse):
        '''Returns True if this BibleRange contains the given BibleVerse, otherwise False.
        '''
        if self.book != bible_verse.book:
            return False
        else:
            return (bible_verse >= self.start and bible_verse <= self.end)

    def split(self, by_chap=True, num_verses=None):
        '''Split this range into a list of smaller consecutive ranges.
        
        If by_chap is true, splits are made end of each chapter.
        If num_verses is specified, splits are made after no more than the specified number of verses.
        If both by_chap and num_verses are specified, splits occur both at chapter boundaries, and after
        the specified number of verses.
        '''
        chap_split = [BibleRange(self.book, self.start.chap, self.start.verse, self.end.chap, self.end.verse)]

        # Start by dividing our initial range into chapters, if requested.
        if by_chap:
            chap_split = []
            for chap in range(self.start.chap, self.end.chap + 1):
                if chap == self.start.chap:
                    start_verse = self.start.verse
                else:
                    start_verse = 1
                if chap == self.end.chap:
                    end_verse = self.end.verse
                else:
                    end_verse = self.end.max_verse(chap)
                chap_split.append(BibleRange(self.book, chap, start_verse, chap, end_verse))
        
        # Next, split our list of ranges into smaller ranges with a max numbers of verses, if requested.
        if num_verses is not None:
            verse_split = []
            for bible_range in chap_split:
                start = BibleVerse(bible_range.book, bible_range.start.chap, bible_range.start.verse)
                end = start.add(num_verses-1)
                while end is not None and end < bible_range.end:
                    verse_split.append(BibleRange(bible_range.book, start.chap, start.verse, end.chap, end.verse))
                    start = end.add(1)
                    end = start.add(num_verses-1)
                verse_split.append(BibleRange(bible_range.book, start.chap, start.verse, bible_range.end.chap, bible_range.end.verse))
            return verse_split
        else:
            return chap_split

    def __repr__(self):
        return str((self.book.abbrev, self.start.chap, self.start.verse, self.end.chap, self.end.verse))
    
    def __str__(self):
        return self.string()

    def string(self, abbrev=False, periods=False, nospace=False, nobook=False):
        '''Returns a string representation of this BibleRange.

        If abbrev is True, the abbreviated name of the book is used (instead of the full name).
        If periods is True, chapter and verse numbers are separated by '.' instead of ':'.
        If nospace is True, no spaces are included in the string.
        If nobook is True, the book name is omitted.
        '''
        return _scripture_text.reference_to_string(self.book.abbrev, self.start.chap, self.start.verse,
                                                   self.end.chap, self.end.verse,
                                                   abbrev, periods, nospace, nobook)


class BibleRangeList:
    '''A list of BibleRanges, with the ability to also group BibleRanges.

    Groups are themselves just BibleRangeLists. They are accessed using the
    groups property and created using append_group(). Adding groups also
    updates the main list, but making any direct changes to the main list
    will remove all stored groups.
    '''
    JOIN_SEP  = "," # Character that separates joined passages (i.e. within a group)
    GROUP_SEP = ";" # Character that separates passage groups (i.e. between groups)

    @classmethod
    def new_from_text(cls, text):
        '''For a text string, return a list of BibleRanges in the text.
        '''
        split_texts = text.split(BibleRangeList.JOIN_SEP)
        
        # For each split string, do the raw parsing into BibleRanges
        split_ranges = []
        for split_text in split_texts:
            ranges = []
            ref_tuples = _scripture_text.extract(split_text)
            for ref_tuple in ref_tuples:
                book = BibleBook(ref_tuple[0])
                start_chap = ref_tuple[1]
                start_verse = ref_tuple[2]
                end_chap = ref_tuple[3]
                end_verse = ref_tuple[4]
                ranges.append(BibleRange(book, start_chap, start_verse, end_chap, end_verse))
            split_ranges.append(ranges)

        # Now iterate over these BibleRanges, collating them into a BibleRangeList for each group.
        group_bible_lists = []
        for split_index in range(len(split_ranges)):
            for i in range(len(split_ranges[split_index])):
                bible_range = split_ranges[split_index][i]
                if split_index == 0:
                    # Each range in the split starts its own group
                    group_bible_lists.append(BibleRangeList([bible_range]))
                else:
                    # The first range in a new split belongs to the previous group
                    if i == 0:
                        prev_bible_list = group_bible_lists[-1]
                        prev_bible_list.append(bible_range)
                    else:
                        # The remaining ranges in the split start their own groups
                        group_bible_lists.append(BibleRangeList([bible_range]))
        
        # Now join the groups together into a final BibleRangeList
        result_bible_range_list = BibleRangeList()
        for group_bible_list in group_bible_lists:
            result_bible_range_list.append_group(group_bible_list)
        return result_bible_range_list

    def __init__(self, bible_ranges=None):
        '''bible_versions is the underlying list of BibleRanges.
        '''
        if bible_ranges is None:
            self._list = []
        else:
            self._list = list(bible_ranges)
        
        self._groups = []
        self._parent = None # If we are a group within a parent BibleRangeList, this is a ref to the parent

    @property
    def groups(self):
        '''Returns a regular list containing BibleRangeLists for each group
        in this BibleRangeList.
        '''
        return self._groups

    def append_group(self, bible_range_list):
        group = BibleRangeList(bible_range_list)
        group._parent = self
        self._groups.append(group)
        self._list.extend(bible_range_list)

    def append(self, item):
        self.insert(len(self), item)

    def __len__(self):
        return len(self._list)

    def insert(self, i, item):
        self._list.insert(i, item)
        self._remove_all_groups() # Directly manipulating the main list removes all groups.

    def _remove_all_groups(self):
        for group in self._groups:
            group._parent = None    # Break circular references for easier garbage-collection
        self._groups = []

    def __getitem__(self, i):
        '''NOTE: When a slice is provided, the resulting sequence is itself an instance of
        BibleRangeList, rather than a generic list.
        '''
        if isinstance(i, slice):
            return self.__class__(self._list[i])
        else:
            return self._list[i]
    
    def __setitem__(self, i, item):
        self._list[i] = item
        self._remove_all_groups() # Directly manipulating the main list removes all groups.

    def __delitem__(self, i):
        del self._list[i]
        self._remove_all_groups() # Directly manipulating the main list removes all groups.

    def string(self, abbrev=False, periods=False, nospace=False, nobook=True, showgroups=True):
        '''Returns a string representation of this BibleRangeList.

        If abbrev is True, the abbreviated name of the book is used (instead of the full name).
        If periods is True, chapter and verse numbers are separated by '.' instead of ':'.
        If nospace is True, no spaces are included in the string.
        If nobook is True, the book name is omitted when it's the same as the previous BibleRange.
        If showgroups is True, grouped passages are joined with the JOIN_STR character.
        '''
        if showgroups and self._parent is not None:
            # We are a subgroup and wish to display as such
            joiner = BibleRangeList.JOIN_SEP + " "
        else:
            # Either we're not a subgroup or we don't want to display as a subgroup
            joiner = BibleRangeList.GROUP_SEP + " "
        strings = []
        if len(self.groups) > 0:
            # Iterating over groups (which are themselves BibleRangeLists)
            for group in self.groups:
                group_string = group.string(abbrev, periods, nospace, nobook, showgroups)
                # if showgroups:
                #     group_string = group_string.replace(joiner[0], BibleRangeList.JOIN_SEP)
                strings.append(group_string)
        else:
            # Iterating over our list items, which are just BibleRanges
            for i in range(len(self)):
                if i == 0:
                    strings.append(self[i].string(abbrev, periods, nospace, nobook=False))
                else:
                    # If the BibleBook of this BibleRange is the same as the previous BibleRange,
                    # omit the book name.
                    item_nobook = nobook and (self[i].book == self[i-1].book)
                    strings.append(self[i].string(abbrev, periods, nospace, item_nobook))

        result_str = joiner.join(strings)
        if nospace:
            result_str = result_str.replace(" ","")
        return result_str

    def __str__(self):
        return self.string()


class BibleReferenceError(MultiscriptException):
    pass


class InvalidReferenceError(MultiscriptException):
    pass


class _ProtestantCanonRenamed(scriptures.texts.base.Text):
    books = {}
    books.update(scriptures.texts.protestant.ProtestantCanon.books)
    books.update({
        # Ensure the books dictionary matches the values of our BibleBook enum above
        # Also change some of the standard titles of books (e.g. Song of Songs, Revelation)
        # Ensure that Jn is a valid abbreviation for John for both John's gospel and 1 John, 2 John, 3 John
        '1sam': ('1 Samuel', '1Sam', '(?:1|I)(?:\s)?Sam(?:uel)?', [28, 36, 21, 22, 12, 21, 17, 22, 27, 27, 15, 25, 23, 52, 35, 23, 58, 30, 24, 42, 15, 23, 29, 22, 44, 25, 12, 25, 11, 31, 13]),
        '2sam': ('2 Samuel', '2Sam', '(?:2|II)(?:\s)?Sam(?:uel)?', [27, 32, 39, 12, 25, 23, 29, 18, 13, 19, 27, 31, 39, 33, 37, 23, 29, 33, 43, 26, 22, 51, 39, 25]),
        '1kgs': ('1 Kings', '1Kgs', '(?:1|I)(?:\s)?K(?:in)?gs', [53, 46, 28, 34, 18, 38, 51, 66, 28, 29, 43, 33, 34, 31, 34, 34, 24, 46, 21, 43, 29, 53]),
        '2kgs': ('2 Kings', '2Kgs', '(?:2|II)(?:\s)?K(?:in)?gs', [18, 25, 27, 44, 27, 33, 20, 29, 37, 36, 21, 21, 25, 29, 38, 20, 41, 37, 37, 21, 26, 20, 37, 20, 30]),
        '1chr': ('1 Chronicles', '1Chr', '(?:1|I)(?:\s)?Chr(?:o(?:n(?:icles)?)?)?', [54, 55, 24, 43, 26, 81, 40, 40, 44, 14, 47, 40, 14, 17, 29, 43, 27, 17, 19, 8, 30, 19, 32, 31, 31, 32, 34, 21, 30]),
        '2chr': ('2 Chronicles', '2Chr', '(?:2|II)(?:\s)?Chr(?:o(?:n(?:icles)?)?)?', [17, 18, 17, 22, 14, 42, 22, 18, 31, 19, 23, 16, 22, 15, 19, 14, 19, 34, 11, 37, 20, 12, 21, 27, 28, 23, 9, 27, 36, 27, 21, 33, 25, 33, 27, 23]),
        'song': ('Song of Songs', 'Song', 'Song(?:\sof\s(?:Songs|Sol(?:omon)?))?', [17, 17, 11, 16, 16, 13, 13, 14]),
        'john': ('John', 'John', '(?<!(?:1|2|3|I)\s)(?<!(?:1|2|3|I))J(?:oh)?n', [51, 25, 36, 54, 47, 71, 53, 59, 41, 42, 57, 50, 38, 31, 27, 33, 26, 40, 42, 31, 25]),
        '1cor': ('1 Corinthians', '1Cor', '(?:1|I)(?:\s)?Cor(?:inthians)?', [31, 16, 23, 21, 13, 20, 40, 13, 27, 33, 34, 31, 13, 40, 58, 24]),
        '2cor': ('2 Corinthians', '2Cor', '(?:2|II)(?:\s)?Cor(?:inthians)?', [24, 17, 18, 18, 21, 18, 16, 24, 15, 18, 33, 21, 14]),
        '1thess': ('1 Thessalonians', '1Thess', '(?:1|I)(?:\s)?Thess(?:alonians)?', [10, 20, 13, 18, 28]),
        '2thess': ('2 Thessalonians', '2Thess', '(?:2|II)(?:\s)?Thess(?:alonians)?', [12, 17, 18]),
        '1tim': ('1 Timothy', '1Tim', '(?:1|I)(?:\s)?Tim(?:othy)?', [20, 15, 16, 16, 25, 21]),
        '2tim': ('2 Timothy', '2Tim', '(?:2|II)(?:\s)?Tim(?:othy)?', [18, 26, 17, 22]),
        '1pet': ('1 Peter', '1Pet', '(?:1|I)(?:\s)?Pet(?:er)?', [25, 25, 22, 19, 14]),
        '2pet': ('2 Peter', '2Pet', '(?:2|II)(?:\s)?Pet(?:er)?', [21, 22, 18]),
        '1john': ('1 John', '1John', '(?:(?:1|I)(?:\s)?)J(?:oh)?n', [10, 29, 24, 21, 21]),
        '2john': ('2 John', '2John', '(?:(?:2|II)(?:\s)?)J(?:oh)?n', [13]),
        '3john': ('3 John', '3John', '(?:(?:3|III)(?:\s)?)J(?:oh)?n', [14]),
        'rev': ('Revelation', 'Rev', 'Rev(?:elation)?(?:\sof Jesus Christ)?', [20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20, 8, 21, 18, 24, 21, 15, 27, 21]),
        })

    def extract(self, text):
        # scriptures package doesn't recognise periods, so we first replace them with colons
        return super().extract(text.replace('.', ':'))

    def reference_to_string(self, bookname, chapter, verse=None,
                            end_chapter=None, end_verse=None,
                            abbrev=False, periods=False, nospace=False, nobook=False):
        '''
        If abbrev is True, the abbreviated name of the book is used (instead of the full name).
        If periods is True, chapter and verse numbers are separated by '.' instead of ':'.
        If nospace is True, no spaces are included in the string.
        If nobook is True, the book name is omitted.
        '''
        result = super().reference_to_string(bookname, chapter, verse, end_chapter, end_verse)
        book_info = self.get_book(bookname)
        if abbrev:
            if nobook:
                result = result.replace(book_info[0] + " ", "")
            else:
                result = result.replace(book_info[0], book_info[1])
        else:
            if nobook:
                result = result.replace(book_info[0] + " ", "")
        if periods:
            result = result.replace(':','.')
        if nospace:
            result = result.replace(' ','')
        return result

_scripture_text = _ProtestantCanonRenamed()

# Dict of scriptures module book info, keyed by BibleBook enum
_info_by_book = {}

def _setup_info_by_book():
    for info in _ProtestantCanonRenamed.books.values():
        book = BibleBook(info[0])
        _info_by_book[book] = info

_setup_info_by_book()

