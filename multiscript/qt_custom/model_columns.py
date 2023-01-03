from enum import Enum, auto

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from multiscript.qt_custom.delegates import EnhancedCheckedDelegate
from multiscript.util.exception import MultiscriptException

class ItemListModelColumn:
    '''An ItemListModelColumn is added to an ItemListTableModel. The column
    specifies how to use the item in each row to get and set the data
    for one column.
    '''
    def __init__(self, type_enum, label, hide=False):
        # We use the type_enum field as a faster way to check column types, rather than
        # relying on isinstance(), which is a slower operation.
        self.type_enum = type_enum
        self.label = label
        self.column_index = None    # Our column index in the table
        self.editable = True        # True if the user can edit the column
        self.hide = hide            # True if views should hide the column
        self.delegate = None        # Can specify a custom delegate for views
        self._model = None          # The ItemListTableModel we belong to.
    
    def set_model(self, model):
        self._model = model
    
    def items_inserted(self, item_list, before_row_index):
        pass

    def items_removed(self, num_rows, start_row_index):
        pass

    def get_data(self, row_index):
        pass

    def set_data(self, row_index, value):
        pass


class ModelColumnType(Enum):
    ATTRIBUTE   = auto()
    BOOLEAN     = auto()
    ALLTEXT     = auto()


class AttributeColumn(ItemListModelColumn):
    '''
    An AttributeColumn typically displays a single attribute of the items in
    each row. The attribute is usally specified by its string name.

    Alternatively, a getter and setter can be supplied, to allow more complex
    data from each item to be displayed in the column and updated. If
    supplied, the getter and setter should have these forms (or equivalent):
        def getter(item):
            return data_to_display_in_this_column
        
        def setter(item, new_value)
            # Update the item using new_value
    '''
    SAME_AS_GET_ATTR = object() # Sentinel
    def __init__(self, label, get_attr_or_func, set_attr_or_func=SAME_AS_GET_ATTR, hide=False):
        '''
        get_attr_or_func can either be a string attribute name, or a callable equivalent to:
            def getter(item):
                return data_to_display_in_this_column

        set_attr_of_func can either be a string attribute name, or a callable equivalent to:
            def setter(item, new_value)
                # Update the item using new_value

        If a string is supplied for get_attr_func, and set_attr_or_func is not supplied,
        the same attribute will be used for both getting and setting.

        If set_attr_or_func is None, or get_attr_or_func is a callable and set_attr_or_func is
        not supplied, the column becomes non-editable (read-only).
        '''
        super().__init__(ModelColumnType.ATTRIBUTE, label, hide)
        self.get_attr_name = None
        self.set_attr_name = None
        self.get_function = None
        self.set_function = None
        self.default_get_func = lambda item: getattr(item, self.get_attr_name)
        self.default_set_func = lambda item, value: setattr(item, self.set_attr_name, value)

        if get_attr_or_func is None:
            raise Exception("get_attr_or_func cannot be None")

        if isinstance(get_attr_or_func, str):
            self.get_attr_name = get_attr_or_func
            self.get_function = self.default_get_func
        elif callable(get_attr_or_func):
            self.get_function = get_attr_or_func
        else:
            raise MultiscriptException("get_attr_or_func must be string or callable")

        if set_attr_or_func is None:
            # Column becomes non-editable
            self.set_function = None
            self.editable = False
        elif isinstance(set_attr_or_func, str):
            self.set_attr_name = set_attr_or_func
            self.set_function = self.default_set_func
        elif callable(set_attr_or_func):
            self.set_function = set_attr_or_func
        elif set_attr_or_func is AttributeColumn.SAME_AS_GET_ATTR:
            # Check there is a get attribute we can also use as the set attribute.
            if self.get_attr_name is not None:
                self.set_attr_name = self.get_attr_name
                self.set_function = self.default_set_func
            else:
                # If there is no get attribute specified, we can't use it
                # as the set attribute. So we make the column not editable.
                self.set_function = None
                self.editable = False
        else:
            raise MultiscriptException("set_attr_or_func must be string or callable")

    def get_data(self, row_index):
        if self.get_function is not None:
            return self.get_function(self._model.items[row_index])

    def set_data(self, row_index, value):
        if self.set_function is not None:
            self.set_function(self._model.items[row_index], value)


class BooleanColumn(ItemListModelColumn):
    '''
    A BooleanColumn doesn't display attributes of an item. Instead, it
    provides an extra column of boolean data, for display as checkboxes
    or radio buttons. The boolean data is stored in this column instance.
    '''

    def __init__(self, label=None, use_radio_buttons=False, default_value=False):
        super().__init__(ModelColumnType.BOOLEAN, label)
        self.use_radio_buttons = use_radio_buttons
        self.default_value = default_value
        self.delegate = EnhancedCheckedDelegate(None, self.use_radio_buttons)
        self.bool_values = []

    def set_model(self, model):
        super().set_model(model)
        self.items_inserted(self._model.items, 0)

    def items_inserted(self, item_list, before_row_index):
        # Ignore the items themselves and just insert the right number of default values
        self.bool_values[before_row_index:before_row_index] = [self.default_value] * len(item_list)

    def items_removed(self, num_rows, start_row_index):
        self.bool_values[start_row_index:start_row_index + num_rows] = []

    def get_data(self, row_index):
        return self.bool_values[row_index]

    def set_data(self, row_index, value):
        self.bool_values[row_index] = value
    
    def count_bool(self, bool_value=True):
        return self.bool_values.count(bool_value)
    
    def true_items(self):
        return [self._model.items[i] for i in range(self._model.rowCount()) if self.bool_values[i]]


class AllTextColumn(ItemListModelColumn):
    '''
    Note: I wrote this class when it seemed that QSortFilterProxyModel could
    only filter on a single column. I've since realised that calling 
    QSortFilterProxyModel.setFilterKeyColumn(-1) will allow filtering on
    all columns. As a result this class is not really needed.
    -----
    An AllTextColumn doesn't directly single attributes of an item. Instead,
    it provides an extra column of text data. The data in this column is
    the collation of display text from all other columns in the row, separated
    by spaces. Typically, an AllTextColumn is hidden and set to be the filter
    column for the table, allowing all-text filtering of the rows in the table.
    The collated text data is stored in this column instance.
    '''
    def __init__(self, label=None):
        super().__init__(ModelColumnType.ALLTEXT, label)
        self.editable = False
        self.hide = True
        self.alltext_values = []

    def set_model(self, model):
        super().set_model(model)
        self.items_inserted(self._model.items, 0)
        self._model.dataChanged.connect(self._on_model_dataChanged)

    def items_inserted(self, item_list, before_row_index):
        self.alltext_values[before_row_index:before_row_index] = [""] * len(item_list)
        self._collate_text(len(item_list), before_row_index)

    def _collate_text(self, num_rows, start_row_index):
        for row_index in range(start_row_index, start_row_index + num_rows):
            alltext = ""
            for column_index in range(self._model.columnCount()):
                if self._model.model_columns[column_index] is not self:
                    index = self._model.index(row_index, column_index, QtCore.QModelIndex())
                    data = self._model.data(index, Qt.ItemDataRole.DisplayRole)
                    alltext += " " + (str(data) if data is not None else "")
            self.alltext_values[row_index] = alltext

    def items_removed(self, num_rows, start_row_index):
        self.alltext_values[start_row_index:start_row_index + num_rows] = []

    def get_data(self, row_index):
        return self.alltext_values[row_index]

    def _on_model_dataChanged(self, topLeftIndex, bottomRightIndex, roleList):
        # Technically we are responding to this changed data by changing our own value, which ought
        # to result in another dataChanged signal being emitted. But in practice, the table view seems
        # to update just fine without the second signal being emitted.
        self._collate_text(bottomRightIndex.row() - topLeftIndex.row() + 1, topLeftIndex.row())
