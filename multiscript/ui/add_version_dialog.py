
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

import multiscript
from multiscript.ui.add_version_dialog_generated import Ui_AddVersionDialog
from multiscript.qt_custom.concurrency import call_nonblock
from multiscript.qt_custom.models import ItemListTableModel, ItemListFilterSortProxyModel
from multiscript.qt_custom.model_columns import AttributeColumn, BooleanColumn


class AddVersionDialog(QtWidgets.QDialog, Ui_AddVersionDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_open = False
        self.pending_results = set()
        self.sources = multiscript.app().all_sources

        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)

        self.refreshButton.clicked.connect(self.refresh_list)
        self.sidebarForm.setVisible(False)
        self.splitter.setStretchFactor(0,1)     # Main panel expands by default
        self.splitter.setStretchFactor(1,0)     # Sidebar panel doesn't expand by default
        self.editButton.toggled.connect(self.on_edit_button_toggled)
        self.filterLineEdit.setFocus(Qt.FocusReason.OtherFocusReason)

        self.versionModel = ItemListTableModel() # Stores a list of BibleVersions
        self.versionModel.append_model_columns([
            BooleanColumn(),
            AttributeColumn("Language",         "lang"),
            AttributeColumn("Abbrev",           "abbrev"),
            AttributeColumn("Version Name",     "name"),
            AttributeColumn("Source",           lambda version: version.bible_source.name)
        ])
        self.versionModel.set_all_columns_editable(False)

        # We use a proxy model for sorting and filtering
        self.proxyModel = ItemListFilterSortProxyModel(None, self.versionModel, self.filterLineEdit)
        self.versionTable.setModel(self.proxyModel)
        self.versionForm.setModel(self.proxyModel)
        self.versionForm.setSelectionModel(self.versionTable.selectionModel())
        
        # Note: The QMenu must receive this window (self) as its parent, otherwise it's actions
        # won't work on Mac, and possibly on other platforms too.
        self.addManualMenu = QtWidgets.QMenu(self)
        for source in self.sources:
            if source.allow_manual_versions:
                action = self.addManualMenu.addAction(f"Add Manual {source.name} Version")
                action.setData(source)
                action.triggered.connect(self.on_add_manual_version_triggered)
        self.addManualButton.setMenu(self.addManualMenu)

    def on_add_manual_version_triggered(self, checked):
        bible_source = self.sender().data()
        self.versionModel.append_items([bible_source.new_bible_version()])
        self.filterLineEdit.clear()
        
        # Select the final row in the table, which will be our new version
        # Note, when creating QModelIndex objects, they link the model they belong to.
        # Therefore, we need to create them on our proxy model, since that's the model
        # that's technically actually being displayed.
        last_row = self.proxyModel.rowCount()-1
        last_col = self.proxyModel.columnCount()-1
        top_left = self.proxyModel.index(last_row, 0)
        bottom_right = self.proxyModel.index(last_row, last_col)
        selection = QtCore.QItemSelection(top_left, bottom_right)
        self.versionTable.selectionModel().select(selection,
            QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect | QtCore.QItemSelectionModel.SelectionFlag.Current)
        self.versionTable.scrollToBottom()

    def tr(self, str):
        return QtWidgets.QApplication.translate(self.__class__.__name__, str, None, -1)

    def showEvent(self, event):
        if not self.is_open:
            self.is_open = True
            self.refresh_list()

        super().showEvent(event)

    def done(self, result):
        self.is_open = False
        self.cleanup()
        super().done(result)

    def refresh_list(self):
        self.versionModel.clear_items()
        self.pending_results.clear()
        self.statusLabel.setText(self.tr("Loading..."))
        self.progressBar.setMaximum(len(self.sources))
        self.progressBar.setValue(0)
        for source in self.sources:
            pending_result = call_nonblock(source.get_all_versions, callback=self.add_versions)
            self.pending_results.add(pending_result)
    
    def add_versions(self, pending_result):
        if pending_result in self.pending_results:
            self.progressBar.setValue(self.progressBar.value() + 1)
            self.pending_results.remove(pending_result)
            self.versionModel.append_items(pending_result.value)
            self.versionTable.resizeColumnsToContents()
        else:
            # Must be a pending result from a previous invocation of the dialog. We ignore it
            pass
        if len(self.pending_results) == 0:
            version_count = self.versionModel.rowCount()
            self.statusLabel.setText(self.tr("Loading finished") +
                                     f" ({version_count} " + self.tr("versions") + ")")

    def cleanup(self):
        self.pending_results.clear()

    def get_versions_to_add(self):
        if self.result() == QtWidgets.QDialog.DialogCode.Rejected:
            return []

        # Set the checkboxes for the selected versions.
        for index in self.versionTable.get_selected_item_indexes():
            self.versionModel.model_columns[0].set_data(index, True)
            
        # Return the checked versions.
        return self.versionModel.model_columns[0].true_items()

    def on_edit_button_toggled(self, checked):
        self.sidebarForm.setVisible(checked)
