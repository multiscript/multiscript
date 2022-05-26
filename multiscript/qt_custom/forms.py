
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt, Signal, Slot

from multiscript.qt_custom.views import get_underlying_model_and_selection
from multiscript.qt_custom.models import ItemListTableModel
from multiscript.qt_custom.delegates import EnhanceDataMapperDelegate


class Form(QtWidgets.QWidget):
    '''A form is a data-aware widget that uses QDataWidgetMapper to
    connect child widgets to fields in an underlying ItemListTableModel.

    Reimplement add_mappings() to add columns to the model that will be associated
    with individual child widgets. Do this by calling add_model_column_and_widget()
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self._outer_model = None
        self._item_list_model = None
        self._selection_model = None
        self._mapped_widgets = None
        self.mapper = QtWidgets.QDataWidgetMapper()
        self.mapper.setItemDelegate(EnhanceDataMapperDelegate())
        self.setAutoSubmit(True)
        
    def setModel(self, model):
        '''Binds the form to a model.
        '''
        # We need the underlying item list model in order to add model columns to it.
        # But the mapper needs the outer model (including any proxy model wrappers)
        # so that it can track the current selection
        self._outer_model = model
        self._item_list_model, selection = get_underlying_model_and_selection(self._outer_model, None)
        if self._item_list_model is None:
            return

        self.mapper.setModel(self._outer_model)
        self._mapped_widgets = set()
        self.add_mappings()

    def setSingleItem(self, item):
        '''Binds the form to a single item, instead of to an underlying model.

        Sets auto submit to false, so you will need to manually call submit().
        '''
        model = ItemListTableModel()
        model.append_item(item)
        self.setModel(model)
        self.setEnabled(True)
        self.mapper.setCurrentIndex(0)
        self.setAutoSubmit(False)

    def setAutoSubmit(self, auto_submit=True):
        if auto_submit:
            self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.AutoSubmit)
        else:
            self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

    @Slot()
    def submit(self):
        '''Calls submit() on the underlying QDataWidgetMapper, and returns the result.
        '''
        return self.mapper.submit()

    def add_mappings(self):
        pass

    def add_model_column_and_widget(self, model_column, widget, col_index=None):
        if self._item_list_model is None:
            return

        if col_index is None:
            col_index = self._item_list_model.columnCount()
        
        if model_column is not None:
            self._item_list_model.append_model_columns([model_column])
    
        self.mapper.addMapping(widget, col_index)
        self._mapped_widgets.add(widget)
        if isinstance(widget, QtWidgets.QLineEdit):
            widget.textEdited.connect(self._on_data_widget_text_edited)
        elif isinstance(widget, QtWidgets.QComboBox):
            widget.editTextChanged.connect(self._on_data_widget_text_edited)
        elif isinstance(widget, QtWidgets.QAbstractSpinBox):
            widget.valueChanged.connect(self._on_data_widget_value_changed)
        elif isinstance(widget, QtWidgets.QAbstractButton):
            widget.toggled.connect(self._on_button_data_widget_toggled)

    def clear_widgets(self):
        for widget in self._mapped_widgets:
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.clearEditText()
            elif isinstance(widget, QtWidgets.QAbstractSpinBox):
                widget.clear()
            elif isinstance(widget, QtWidgets.QAbstractButton):
                widget.setChecked(False)

    def setSelectionModel(self, selectionModel):
        '''Allows the item the form is editing to track a selection model.
        '''
        self._selection_model = selectionModel
        self._selection_model.selectionChanged.connect(self._on_selection_changed)
    
    def _on_selection_changed(self, selected, deselected):
        selected_rows = self._selection_model.selectedRows()
        if len(selected_rows) > 0:
            self.setEnabled(True)
            # Just place the first selected row in the edit form
            self.mapper.setCurrentIndex(selected_rows[0].row())
        else:
            self.setEnabled(False)
            self.mapper.setCurrentIndex(-1)
            self.clear_widgets()
    
    def _on_button_data_widget_toggled(self, checked):
        self.mapper.submit()
    
    def _on_data_widget_text_edited(self, text):
        # If we wanted to submit on every keystroke, we would do so here.
        # self.mapper.submit()
        pass
    
    def _on_data_widget_value_changed(self, value):
        # If we wanted to submit on every keystroke, we would do so here.
        # self.mapper.submit()
        pass