
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt

from multiscript.qt_custom.model_columns import ModelColumnType


class ItemListTableModel(QtCore.QAbstractTableModel):
    '''
    A QAbstractTableModel for handling table data whose rows represent a
    list of items, and whose columns are usually attributes of those items.
    The model stores the list of items internally.

    To allow the items to be displayed, call insert_model_columns() or
    append_model_columns() to add ItemListModelColumn instances to this
    model. Each ItemListModelColumn determines how to use the item in
    each row to get and set data for that column.
    '''
    SORT_ROLE = Qt.UserRole

    def __init__(self):
        super().__init__()
        self.showRowNumbers = False
        self.rowHeaderText = "  "       # Gives us some width to allow for moving, if enabled.
        self.items = []                 # The list of items to store
        self.model_columns = []
        self.columns_by_type = {}       # Keys: ModelColumnType. Values: List of columns in (logical) order

        self._rebuild_column_metadata()

    def _rebuild_column_metadata(self):
        self.columns_by_type = {}
        for column_type in ModelColumnType:
            self.columns_by_type[column_type] = []
        
        for column_index in range(len(self.model_columns)):
            column = self.model_columns[column_index]
            column.column_index = column_index
            self.columns_by_type[column.type_enum].append(column)            

    def rowCount(self, parent=None):
        return len(self.items)
    
    def columnCount(self, parent=None):
        return len(self.model_columns)

    def show_all_columns(self, show=True):
        for column in self.model_columns:
            column.hide = not show

    def hide_all_columns(self, hide=True):
        for column in self.model_columns:
            column.hide = hide

    def set_all_columns_editable(self, editable=True):
        for column in self.model_columns:
            column.editable = editable

    def insert_model_column(self, model_column, before_col_index):
        self.insert_model_columns([model_column], before_col_index)

    def append_model_column(self, model_column):
        self.append_model_columns([model_column])

    def remove_model_column(self, col_index):
        self.remove_model_columns(1, col_index)

    def append_model_columns(self, columns_list):
        self.insert_model_columns(columns_list, self.columnCount())

    def clear_model_columns(self):
        self.remove_model_columns(self.columnCount(), 0)

    def insert_item(self, item, before_row_index):
        self.insert_items([item], before_row_index)

    def append_item(self, item):
        self.append_items([item])

    def remove_item(self, row_index):
        self.remove_items(1, row_index)

    def append_items(self, item_list_to_append):
        self.insert_items(item_list_to_append, self.rowCount())

    def clear_items(self):
        self.remove_items(self.rowCount(), 0)

    def insert_model_columns(self, columns_list, before_col_index):
        self.beginInsertColumns(QtCore.QModelIndex(), before_col_index, before_col_index + len(columns_list) - 1)
        self.model_columns[before_col_index:before_col_index] = columns_list
        for column in columns_list:
            column.set_model(self)
        self._rebuild_column_metadata()
        self.endInsertColumns()
    
    def remove_model_columns(self, num_columns, start_col_index):
        self.beginRemoveColumns(QtCore.QModelIndex(), start_col_index, start_col_index + num_columns - 1)
        # We just throw the removed columns away, allowing them to be garbage-collected
        self.model_columns[start_col_index:start_col_index + num_columns] = []
        self._rebuild_column_metadata()
        self.endRemoveColumns()

    def insert_items(self, item_list, before_row_index):
        self.beginInsertRows(QtCore.QModelIndex(), before_row_index, before_row_index + len(item_list) - 1)
        self.items[before_row_index:before_row_index] = item_list
        for column in self.model_columns:
            column.items_inserted(item_list, before_row_index)
        self.endInsertRows()

    def remove_items(self, num_rows, start_row_index):
        self.beginRemoveRows(QtCore.QModelIndex(), start_row_index, start_row_index + num_rows - 1)
        # We just throw the removed items away, allowing them to be garbage-collected
        self.items[start_row_index:start_row_index + num_rows] = []
        for column in self.model_columns:
            column.items_removed(num_rows, start_row_index)
        self.endRemoveRows()

    def data(self, index, role=Qt.DisplayRole):
        data = self.model_columns[index.column()].get_data(index.row())

        # For boolean data, we don't display it as a string. Instead
        # we display it using the Qt.CheckStateRole.
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if type(data) is bool:
                return None
            else:
                return data
        elif role == Qt.CheckStateRole:
            if type(data) is bool:
                return Qt.Checked if data else Qt.Unchecked
        elif role == ItemListTableModel.SORT_ROLE:
            if type(data) is bool:
                # When sorting ascending, put True before False
                return -1 if data == True else 0
            else:
                return data
        else:
            return None

    def setData(self, index, value, role=Qt.EditRole):
        result = None
        if role == Qt.DisplayRole or role == Qt.EditRole or role == Qt.CheckStateRole:
            if role == Qt.CheckStateRole:
                value = True if value == Qt.Checked else False

            self.model_columns[index.column()].set_data(index.row(), value)
            self.dataChanged.emit(index, index, [role])
            result = True
        else:
            result = super().setData(index, value, role)
        return result

    def flags(self, index):
        data = self.model_columns[index.column()].get_data(index.row())
        result_flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
        if type(data) is bool:
            result_flags |= Qt.ItemIsUserCheckable
        elif self.model_columns[index.column()].editable:
            result_flags |= Qt.ItemIsEditable

        return result_flags

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        header = None
        if role == Qt.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                header = self.model_columns[section].label
            elif orientation == Qt.Orientation.Vertical:
                if self.showRowNumbers:
                    header = section + 1 # sections are indexed from 0
                else:
                    header = self.rowHeaderText
        else:
            header = super().headerData(section, orientation, role)
        
        return header


class ItemListFilterSortProxyModel(QtCore.QSortFilterProxyModel):
    
    def __init__(self, parent=None, sourceModel=None, lineEditWidget=None):
        super().__init__(parent)
        if sourceModel is not None:
            self.setSourceModel(sourceModel)
        if lineEditWidget is not None:
            self.setLineEditWidget(lineEditWidget)

    def setSourceModel(self, sourceModel):
        super().setSourceModel(sourceModel)

        # Unwrap any other proxy models to get the underlying model
        while isinstance(sourceModel, QtCore.QAbstractProxyModel):
            sourceModel = sourceModel.sourceModel()

        if isinstance(sourceModel, ItemListTableModel):
            self.setSortRole(ItemListTableModel.SORT_ROLE)        

            # We wish to set filtering on all columns. The easiest way to do so
            # is to call setFilterKeyColumn(-1). Before I realised this was possible
            # I created my own solution using an AllTextColumn. The code below
            # uses an AllTextColumn if present, otherwise it simply calls
            # setFilterKeyColumn(-1)
            alltext_columns = sourceModel.columns_by_type[ModelColumnType.ALLTEXT]
            if len(alltext_columns) > 0:
                first_alltext_column = alltext_columns[0]
                self.setFilterKeyColumn(first_alltext_column.column_index)
                print(first_alltext_column.column_index)
            else:
                self.setFilterKeyColumn(-1)

    def setLineEditWidget(self, lineEditWidget):
        self.setFilterRegExp(lineEditWidget.text())
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        lineEditWidget.textChanged.connect(self.on_filterLineEdit_textChanged)

    def on_filterLineEdit_textChanged(self, string):
        wildcard_str = string.strip()
        self.setFilterWildcard(wildcard_str)
