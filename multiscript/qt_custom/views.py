from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from multiscript.qt_custom.models import ItemListTableModel

MAX_COLUMN_WIDTH = 600

class ItemListTableView(QtWidgets.QTableView):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.standard_delegate = self.itemDelegate() # We save this so we can restore it later
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.horizontalHeader().setMaximumSectionSize(MAX_COLUMN_WIDTH)

    def setModel(self, model):
        super().setModel(model)
        self.set_any_column_delegates()
        self.configure_new_columns(0, model.columnCount()-1)

        # For some reason, overriding the rowCountChanged() and columnCountChanged()
        # slots doesn't result in them being called. So here we connect to the
        # model's signals instead.
        # NOTE: The rowsInserted and rowsRemoved signals are rapidly called many, many times
        # when a using a proxy model for filtering. These signals must be very efficient, or
        # the whole UI becomes extremely sluggish.
        model.rowsInserted.connect(self.on_rows_inserted)
        model.rowsRemoved.connect(self.on_rows_removed)
        model.columnsInserted.connect(self.on_cols_inserted)
        model.columnsRemoved.connect(self.on_cols_removed)

        # We need these signals to ensuring we set and clear custom column delegates correctly.
        model.columnsAboutToBeInserted.connect(self.on_cols_about_to_be_inserted)
        model.columnsAboutToBeRemoved.connect(self.on_cols_about_to_be_removed)

    def on_rows_inserted(self, parent, first, last):
        # A viewport update seems to be needed sometimes when rows are inserted or removed,
        # as the table view grid does not always paint correctly.
        self.viewport().update()

    def on_rows_removed(self, parent, first, last):
        # A viewport update seems to be needed sometimes when rows are inserted or removed,
        # as the table view grid does not always paint correctly.
        self.viewport().update()

    def on_cols_about_to_be_inserted(self, parent, first, last):
        # Custom column delegates are set against column indexes. However, when columns are
        # inserted or removed, Qt's internal list of which columns have custom
        # delegates doesn't seem to change, even though we'd like it to adapt to the changed
        # columns. Therefore, it's most reliable to remove all our custom column delegates
        # just before adding/removing columns, and then setting all our custom column
        # delegates again after the columns are added/removed.
        self.clear_all_column_delegates()

    def on_cols_inserted(self, parent, first, last):
        # Custom column delegates are set against column indexes. However, when columns are
        # inserted or removed, Qt's internal list of which columns have custom
        # delegates doesn't seem to change, even though we'd like it to adapt to the changed
        # columns. Therefore, it's most reliable to remove all our custom column delegates
        # just before adding/removing columns, and then setting all our custom column
        # delegates again after the columns are added/removed.        
        self.set_any_column_delegates()

        self.configure_new_columns(first, last)

        # An update seems to be needed sometimes when columns are inserted or removed,
        # as the table view grid does not always paint correctly.
        self.viewport().update()

    def on_cols_about_to_be_removed(self, parent, first, last):
        # Custom column delegates are set against column indexes. However, when columns are
        # inserted or removed, Qt's internal list of which columns have custom
        # delegates doesn't seem to change, even though we'd like it to adapt to the changed
        # columns. Therefore, it's most reliable to remove all our custom column delegates
        # just before adding/removing columns, and then setting all our custom column
        # delegates again after the columns are added/removed.
        #
        # Note too that if we don't remove custom delegates before removing the column they
        # belong to, we will usually crash. When the column is removed our custom delegate will
        # usually by garbage-collected by Python. However, it would still be registered with
        # Qt, which will try to call it, which results in a segfault 11! So we must remove it now.
        self.clear_all_column_delegates()

    def on_cols_removed(self, parent, first, last):
        self.set_any_column_delegates()
        # An update seems to be needed sometimes when columns are inserted or removed,
        # as the table view grid does not always paint correctly.
        self.viewport().update()

    def clear_all_column_delegates(self):
        for column_index in range(self.model().columnCount()):
            self.setItemDelegateForColumn(column_index, None)

    def set_any_column_delegates(self):
        model = get_underlying_model(self.model())
        if model is None:
            return
        for column_index in range(model.columnCount()):
            model_column = model.model_columns[column_index]
            if model_column.delegate is not None:
                self.setItemDelegateForColumn(column_index, model_column.delegate)

    def configure_new_columns(self, first, last):
        '''Apply any relevant model_column settings to the columns in this view.
        first and last specify the columns to configure (inclusive).
        '''
        model = get_underlying_model(self.model())
        if model is None:
            return

        for column_index in range(first, last + 1):
            model_column = model.model_columns[column_index]    
            self.setColumnHidden(column_index, model_column.hide)

    def get_selected_items(self):
        '''Returns a list of the selected items in the underlying ItemListTableModel.
        '''
        selected_items = []
        model = get_underlying_model(self.model())
        if model is None:
            return selected_items
        
        selected_item_indexes = self.get_selected_item_indexes()
        selected_items = [model.items[index] for index in selected_item_indexes]
        return selected_items

    def get_selected_item_indexes(self):
        '''Returns a list of the indexes of selected items in the underlying ItemListTableModel.
        '''
        selected_item_indexes = []
        model, selection = get_underlying_model_and_selection(self.model(), self.selectionModel().selection())
        if model is None:
            return selected_item_indexes # i.e. an empty list

        # We don't need a list of every cell that's selected.
        # Instead, we just need to know which rows are selected.
        # Therefore, we'll ignore every column except the first one.
        indexes = selection.indexes()
        for index in indexes:
            if index.column() == 0:
                selected_item_indexes.append(index.row())

        return selected_item_indexes

    def get_item(self, model_index):
        '''Returns the item in the underlying ItemListTableModel for the given model_index in the view.
        '''
        model, inner_model_index = get_underlying_model_and_index(self.model(), model_index)
        if model is None:
            return None
        
        return model.items[inner_model_index.row()]

    def get_item_index(self, model_index):
        '''Returns the index of the item in the underlying ItemListTableModel for the given model_index in the view.
        '''
        model, inner_model_index = get_underlying_model_and_index(self.model(), model_index)
        if model is None:
            return None
        
        return inner_model_index.row()        

    def get_items_in_display_order(self):
        '''NOTE: This method only works when an ItemListTableModel is directly set on the view,
        with no proxy wrapping of the model.
        '''
        items = []
        for display_row_index in range(self.model().rowCount()):
            logical_row_index = self.verticalHeader().logicalIndex(display_row_index)
            items.append(self.model().items[logical_row_index])
        return items

    def get_item_indexes_in_display_order(self):
        '''NOTE: This method only works when an ItemListTableModel is directly set on the view,
        with no proxy wrapping of the model.
        '''
        item_indexes = []
        for display_row_index in range(self.model().rowCount()):
            logical_row_index = self.verticalHeader().logicalIndex(display_row_index)
            item_indexes.append(logical_row_index)
        return item_indexes
    
    def dataChanged(self, topLeft, bottomRight, roles):
        super().dataChanged(topLeft, bottomRight, roles)

        # For some reason, if the underlying QTableView is not in focus
        # it won't update with the new data unless we expliticly call
        # self.viewport().update(). Calling self.update() is not sufficient.
        # This may be a QT bug. See
        # https://stackoverflow.com/questions/20256493/qtableview-doesnt-respond-to-datachanged-when-not-focused
        self.viewport().update()

    def refresh(self, resize_cols=False):
        '''Repaint the view and its viewport. Some platforms (such as macOS) can have visual glitches
        when rows or columns are updated. They are usually fixed by repainting (not merely updating).
        Note that repainting can be a relatively expensive operation, so this method should only be
        called at the end of a batch of changes, rather than repeatedly after many small changes.
        '''
        if resize_cols:
            self.resizeColumnsToContents()

        self.repaint()
        self.viewport().repaint()
        
#
# Module-level functions
#

def get_underlying_model(outer_model):
    '''Returns the underlying ItemListTableModel.

    If there is no underlying ItemListTablemModel, returns None.
    '''
    model = outer_model

    # Unwrap any proxy models to get the underlying model.
    while isinstance(model, QtCore.QAbstractProxyModel):
        model = model.sourceModel()

    if not isinstance(model, ItemListTableModel):
        model = None
    
    return model

def get_underlying_model_and_selection(outer_model, outer_selection):
    '''Returns a tuple of the underlying ItemListTableModel, and its selection,
    after any proxy models are unwrapped.

    If there is no underlying ItemListTablemModel, returns a tuple of (None, None).
    '''
    model = outer_model
    selection = outer_selection

    # Unwrap any proxy models to get the underlying model, mapping selections
    # as we go.
    while isinstance(model, QtCore.QAbstractProxyModel):
        if selection is not None:
            selection = model.mapSelectionToSource(selection)
        model = model.sourceModel()

    if not isinstance(model, ItemListTableModel):
        model = None
        selection = None
    
    return model, selection

def get_underlying_model_and_index(outer_model, outer_model_index):
    '''Returns a tuple of the underlying ItemListTableModel, and the model_index that corresponds
    to the outer_model and its outer_model_index

    If there is no underlying ItemListTablemModel, returns a tuple of None, None
    '''
    model = outer_model
    model_index = outer_model_index

    # Unwrap any proxy models to get the underlying model, mapping the model_index
    # as we go.
    while isinstance(model, QtCore.QAbstractProxyModel):
        if model_index is not None:
            model_index = model.mapToSource(model_index)
        model = model.sourceModel()

    if not isinstance(model, ItemListTableModel):
        model = None
        model_index = None
    
    return model, model_index

