
from collections import namedtuple
from collections.abc import MutableSequence
from operator import attrgetter

from multiscript.plan.symbols import column_symbols


def get_all_version_combos(version_columns):
    '''For the given list of VersionColumns, returns a list of all the possible VersionCombos.

    Each element of the returned list is a BibleVersionCombo, which it itself a sequence of
    VersionComboElements. A BibleVersionComboElement is a tuple of a BibleVersionColumn and a
    BibleVersion selected from that column.
    
    If version_columns does not contain enough information to generate combinations, this method
    returns an empty list.

    The VersionCombos are returned in an order where the longest columns are varied first,
    which allows the minimum number of templates to be used.
    '''
    version_combos = []
    sorted_cols = sorted(version_columns, key=lambda version_column: len(version_column))

    if version_columns is None or len(version_columns) == 0:
        return []

    if len(sorted_cols[-1]) == 0:
        # The longest column is empty, so all columns are empty
        return []

    # Create a list of counters to iterate through the rows of version in each column
    # Initialise counters to 0, or None for empty columns
    row_counters = [0 if len(col) > 0 else None for col in sorted_cols]
    proceed = True
    while proceed:
        # Collate the version combination for the current row counter values
        version_combo = BibleVersionCombo()
        for i in range(len(sorted_cols)):
            version_col = sorted_cols[i]
            version = None
            if row_counters[i] is not None:
                version = version_col[row_counters[i]]
            combo_element = BibleVersionComboElement(version_col, version)
            version_combo.append(combo_element)
        version_combo.sort_by_col_symbol() # Easier to display the combo when it's in symbol order
        version_combos.append(version_combo)

        # Increment the row_counters, with carrying
        col_to_increment = len(row_counters) - 1 # Increment the right-most counter first
        increment_complete = False
        while not increment_complete:
            # If this counter is None, move left one column
            if row_counters[col_to_increment] is None:
                col_to_increment -= 1
                if col_to_increment < 0:
                    # We're overflowing the left-most counter, so we've enumerated all the VersionCombos
                    increment_complete = True
                    proceed = False
                    continue
                continue

            row_counters[col_to_increment] += 1
            if row_counters[col_to_increment] < len(sorted_cols[col_to_increment]):
                increment_complete = True
            else:
                # Carry
                row_counters[col_to_increment] = 0 # Current column counter overflows back to 0
                col_to_increment -= 1              # Move left one column
                if col_to_increment < 0:
                    # We're overflowing the left-most counter, so we've enumerated all the VersionCombos
                    increment_complete = True
                    proceed = False

    return version_combos


class BibleVersionColumn(MutableSequence):
    '''A list of BibleVersions selected for use in a column. The column is specified by its symbol_index.
    
    Note that two VersionColumns only compare equal if they are the same object. Their contents are
    not compared.
    '''
    def __init__(self, bible_versions=None, symbol_index=None):
        '''bible_versions is the underlying list of BibleVersions.
        symbol_index is the index into the list of column symbols for the symbol of this column.
        '''
        if bible_versions is None:
            self.data = []
        else:
            self.data = list(bible_versions)
        
        if symbol_index is None:
            self.symbol_index = 0
        else:
            self.symbol_index = symbol_index

    def __len__(self):
        return len(self.data)

    def insert(self, i, item):
        self.data.insert(i, item)

    def __getitem__(self, i):
        '''NOTE: When a slice is provided, the resulting sequence is itself an instance of
        BibleVersionColumn, rather than a generic list.
        '''
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]
    
    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]


class BibleVersionCombo(MutableSequence):
    '''A list of VersionComboElements.
    '''
    def __init__(self, version_combo_elements=None):
        if version_combo_elements is None:           # The underlying list of BibleVersionComboElements
            self.data = []
        else:
            self.data = list(version_combo_elements)

    def __len__(self):
        return len(self.data)

    def insert(self, i, item):
        self.data.insert(i, item)

    def __getitem__(self, i):
        '''NOTE: When a slice is provided, the resulting sequence is itself an instance of
        BibleVersionCombo, rather than a generic list.
        '''
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]
    
    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]
    
    def copy(self):
        return self.__class__(self)

    def __eq__(self, other):
        try:
            return (self.data == other.data)
        except:
            return False

    def __repr__(self):
        return repr(self.data)

    def sort_by_col_symbol(self):
        self.data.sort(key=attrgetter('version_column.symbol_index'))

    def sort_by_col_length(self):
        self.data.sort(key=lambda combo_element: len(combo_element.version_column))
    
    @property
    def template_combo(self):
        '''Returns the BibleVersionCombo that should be used as the template for this
        BibleVersionCombo. In general, the template combo is the same as this version
        combo, except that the version of the longest non-None column is set to
        None.
        
        If the base template should be used, this property returns None.
        '''
        template_combo = self.copy()
        template_combo.sort_by_col_length()
        use_base_template = True
        for i in reversed(range(len(template_combo))):
            element = template_combo[i]
            if element.version is not None:
                if len(element.version_column) < 2:
                    # Once we reach columns of length 0 or 1, it's time to break out and
                    # use the base template
                    break
                else:
                    # Replace the element with a duplicate except the version is set to None
                    template_combo[i] = BibleVersionComboElement(element.version_column, None)
                    use_base_template = False
                    break               
        
        if use_base_template:
            template_combo = None
        else:
            # In general, sorting by column symbol makes the combination easier to read
            template_combo.sort_by_col_symbol()

        return template_combo


class BibleVersionComboElement(namedtuple('BibleVersionComboElement', ['version_column', 'version'])):
    __slots__ = () # Ensures our subclassed named tuple is immutable (and therefore better for hashing)
                   # See https://docs.python.org/3/library/collections.html#collections.namedtuple
    def __repr__(self):
        version_str = self.version.abbrev if self.version is not None else str(None)
        return column_symbols[self.version_column.symbol_index] + ": " + version_str
