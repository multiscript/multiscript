
import pathlib
import sys

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

import multiscript
from multiscript.bible.reference import BibleRangeList
from multiscript import plan
from multiscript.plan.symbols import column_symbols
from multiscript.qt_custom.models import ItemListTableModel
from multiscript.qt_custom.model_columns import ModelColumnType, AttributeColumn, BooleanColumn
from multiscript.ui.main_window_generated import Ui_MainWindow
from multiscript.ui.add_version_dialog import AddVersionDialog
from multiscript.ui.edit_version_dialog import EditVersionDialog
from multiscript.ui.about_dialog import AboutDialog
from multiscript.ui.plan_config_dialog import PlanConfigDialog
from multiscript.ui.app_config_dialog import AppConfigDialog
from multiscript.ui.plan_notes_dialog import PlanNotesDialog
from multiscript.ui.progress_dialog import ProgressDialog
from multiscript.ui.plan_errors_dialog import PlanErrorsDialog
from multiscript.util.util import launch_file

# TODO: Write some new BibleSources that use free APIs
# TODO: Allow templates to be attached (embedded in) the plan.

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        # Calling code should next call load_plan()

    def tr(self, str):
        return QtWidgets.QApplication.translate(self.__class__.__name__, str, None, -1)

    def setupUi(self):
        super().setupUi(self)
        self.plan = None

        self.appIconLabel.setIcon(self.windowIcon())

        # Mac style leaves too much vertical space, so we reduce it
        if multiscript.on_mac():
            self.centralWidgetLayout.setSpacing(0)
            left, top, right, bottom = self.pathsLayout.getContentsMargins()
            self.pathsLayout.setContentsMargins(left, top, right, 6)
            left, top, right, bottom = self.footerLayout.getContentsMargins()
            self.footerLayout.setContentsMargins(left, 12, right, bottom)
            self.titleAreaWidgetLayout.setSpacing(0)
            left, top, right, bottom = self.moreButtonLayout.getContentsMargins()
            self.moreButtonLayout.setContentsMargins(left, 6, right, bottom)
            
            self.mainAreaWidgetLayout.setSpacing(6)
            left, top, right, bottom = self.mainAreaWidgetLayout.getContentsMargins()
            self.mainAreaWidgetLayout.setContentsMargins(left, top, right, 0)
            self.versionsVerticalLayout.setSpacing(0)

        #
        # Connect signals and slots
        #
        self.newAction.triggered.connect(self.on_new_triggered)
        self.openAction.triggered.connect(self.on_open_triggered)
        self.closeAction.triggered.connect(self.close)
        self.saveAction.triggered.connect(self.on_save_triggered)
        self.saveAsAction.triggered.connect(self.on_save_as_triggered)
        self.restartAction.triggered.connect(self.on_restart_triggered)
        self.exitAction.triggered.connect(QtWidgets.QApplication.closeAllWindows)
        self.undoAction.triggered.connect(self.on_undo_triggered)
        self.redoAction.triggered.connect(self.on_redo_triggered)
        self.cutAction.triggered.connect(self.on_cut_triggered)
        self.copyAction.triggered.connect(self.on_copy_triggered)
        self.pasteAction.triggered.connect(self.on_paste_triggered)
        self.clearAction.triggered.connect(self.on_clear_triggered)
        self.selectAllAction.triggered.connect(self.on_select_all_triggered)
        self.planConfigAction.triggered.connect(self.on_plan_config_triggered)
        self.appConfigAction.triggered.connect(self.on_app_config_triggered)
        self.aboutAction.triggered.connect(self.on_about_triggered)
 
        self.morePlanNotesButton.clicked.connect(self.edit_plan_notes)
        self.addRowsButton.clicked.connect(self.on_add_rows_button_clicked)
        self.removeRowsButton.clicked.connect(self.on_remove_rows_button_clicked)
        self.editButton.clicked.connect(self.on_edit_button_clicked)
        self.addColumnButton.clicked.connect(self.add_version_column)
        self.removeColumnButton.clicked.connect(self.remove_version_column)
        self.templateSelectButton.clicked.connect(self.on_template_browse_button_clicked)
        self.templateShowButton.clicked.connect(self.on_template_show_button_clicked)
        self.outputDirSelectButton.clicked.connect(self.on_output_dir_browse_button_clicked)
        self.outputDirShowButton.clicked.connect(self.on_output_dir_show_button_clicked)
        self.planConfigButton.clicked.connect(self.on_plan_config_triggered)
        self.closeButton.clicked.connect(self.close)
        self.startButton.clicked.connect(self.on_start_button_clicked)
  
        self.passagesLineEdit.textEdited.connect(self.set_plan_changed)

        #
        # Set up models and views
        #
        self.versionModel = ItemListTableModel() # Stores a list of BibleVersions
        self.versionModel.append_model_columns([
            AttributeColumn(self.tr("Abbrev"),           "abbrev"),
            AttributeColumn(self.tr("Version Name"),     "name"),
            AttributeColumn(self.tr("Language"),         "lang"),
            AttributeColumn(self.tr("Source"),           lambda version: version.bible_source.name),
            AttributeColumn(self.tr("Notes"),            "notes")
        ])
        self.versionModel.set_all_columns_editable(False)

        self.versionTable.setModel(self.versionModel)
        self.versionTable.horizontalHeader().setSectionsMovable(True)
        self.versionTable.verticalHeader().setSectionsMovable(True)
        self.versionTable.doubleClicked.connect(self.on_version_table_double_clicked)

    #
    # Plan notes methods
    #

    def edit_plan_notes(self):
        plan_notes_dialog = PlanNotesDialog(None)
        plan_notes_dialog.setNotes(self.plan.notes)
        result = plan_notes_dialog.exec()
        if result == QtWidgets.QDialog.Accepted:
            self.plan.notes = plan_notes_dialog.getNotes()
            self.set_plan_changed()

    #
    # Version table methods
    #

    def get_all_version_columns(self):
        # BooleanColumns that represent a list of BibleVersions can be identified by
        # their extra attribute: col_symbol_index
        bool_columns = self.versionModel.columns_by_type[ModelColumnType.BOOLEAN]
        version_columns = [col for col in bool_columns if hasattr(col, "col_symbol_index")]
        return version_columns

    def add_version_column(self):
        version_columns = self.get_all_version_columns()
        if len(version_columns) == len(column_symbols):
            # We've run out of column symbols, so we don't allow add any more columns
            return

        new_col_symbol_index = len(version_columns)
        new_col_symbol = column_symbols[new_col_symbol_index]
        new_column = BooleanColumn(self.tr("Version") + " " + new_col_symbol)
        new_column.editable = False
        # For BooleanColumns representing a list of BibleVersions, we add an extra attribute
        # specifying the symbol index (which we'll pass to the run data later). It also serves
        # to identify which Boolean columns represent BibleVersions.
        new_column.col_symbol_index = new_col_symbol_index
        
        new_col_index = 0
        if len(version_columns) == 0:
            # This is the first version column. Hard-code to insert before existing column 2
            new_col_index = 2
        else:
            # Find the index of the last existing version column and insert after that
            new_col_index = version_columns[-1].column_index + 1

        self.versionModel.insert_model_column(new_column, new_col_index)
        self.versionTable.resizeColumnToContents(new_col_index)
        self.versionTable.refresh()
        self.set_plan_changed()

        return new_column

    def remove_version_column(self):
        version_columns = self.get_all_version_columns()
        if len(version_columns) == 1:
            # If there's only one version column left, don't remove it.
            return

        # Find the last existing version column and remove it
        last_vers_col_index = version_columns[-1].column_index
        self.versionModel.remove_model_column(last_vers_col_index)
        self.versionTable.refresh()
        self.set_plan_changed()

    def remove_all_version_columns(self):
        # Called when we're loading a plan, and want to clear out all the existing version columns.
        # In this case, we allow all the version columns to be removed.
        version_columns = self.get_all_version_columns()
        for version_column in version_columns:
            self.versionModel.remove_model_column(version_column.column_index)
        self.versionTable.refresh()
        self.set_plan_changed()

    def on_add_rows_button_clicked(self):
        add_version_dialog = AddVersionDialog(None)
        add_version_dialog.exec()
        versions_to_add = add_version_dialog.get_versions_to_add()
        if len(versions_to_add) > 0:
            self.versionModel.append_items(versions_to_add)
            self.versionTable.refresh(resize_cols=True)
            self.set_plan_changed()

    def on_remove_rows_button_clicked(self):
        # We get the selected (row) indexes, and sort them in descending order.
        # This is because we need to remove the selected rows from last to first.
        # (If we remove the selected rows from first to last, the indexes of the remaining
        # selected rows will change.)
        selected_indexes = sorted(self.versionTable.get_selected_item_indexes(), reverse=True)
        if len(selected_indexes) == 0:
            return
        
        for index in selected_indexes:
            self.versionModel.remove_item(index)
        self.versionTable.refresh(resize_cols=True)
        self.set_plan_changed()

    def on_edit_button_clicked(self):
        selected_indexes = self.versionTable.get_selected_item_indexes()
        if len(selected_indexes) > 0:
            # Just edit the first selected version
            self.edit_version(selected_indexes[0])

    def on_version_table_double_clicked(self, model_index):
        self.edit_version(self.versionTable.get_item_index(model_index))

    def edit_version(self, item_index):
        version = self.versionModel.items[item_index]
        edit_version_dialog = EditVersionDialog(None, version)
        result = edit_version_dialog.exec()
        if result == QtWidgets.QDialog.Accepted:
            self.set_plan_changed()

    #
    # Template and Output Folder methods
    #

    def on_template_show_button_clicked(self, checked):
        if self.plan.template_path is not None and self.plan.template_path.exists():
            launch_file(self.plan.template_path.parent)

    def on_output_dir_show_button_clicked(self, checked):
        if self.plan.output_dir_path is not None and self.plan.output_dir_path.exists():
            launch_file(self.plan.output_dir_path)

    def on_template_browse_button_clicked(self, checked):
        filters = ' '.join([('*' + ext) for ext in multiscript.app().all_accepted_template_exts])
        template_path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select Template"),
                                                                   str(self.plan.template_path), filters)
        if len(template_path) > 0:
            self.plan.template_path = pathlib.Path(template_path)
            self.set_plan_changed()

    def on_output_dir_browse_button_clicked(self, checked):
        output_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select Destination Folder"),
                                                                   str(self.plan.output_dir_path))
        if len(output_dir_path) > 0:
            self.plan.output_dir_path = pathlib.Path(output_dir_path)
            self.set_plan_changed()

    #
    # Plan methods
    #

    def on_start_button_clicked(self):
        #
        # Validate window data
        #
        if len(BibleRangeList.new_from_text(self.passagesLineEdit.text())) == 0:
            # No Bible passages
            self.passagesLineEdit.setStyleSheet("border: 2px solid red")
            return
        else:
            self.passagesLineEdit.setStyleSheet("")
        
        if self.versionModel.rowCount() == 0:
            # No versions
            self.versionTable.setStyleSheet("QTableView {border: 2px solid red}")
            return
        else:
            self.versionTable.setStyleSheet("")            

        #
        # Proceed with plan
        #
        self.copy_window_to_plan()
        
        if multiscript.app().app_config_group.general.save_plans_before_execution:
            self.save_plan()

        progress_dialog = ProgressDialog(None, self.plan)
        progress_dialog.exec()

    def load_plan(self, path=None, new_plan=False):
        # Check if we need to save the existing plan
        cancel = False
        if self.plan is not None and self.plan.changed:
            result = self.check_for_save()
            if result == QtWidgets.QMessageBox.Save:
                self.save_plan()
                cancel = False
            elif result == QtWidgets.QMessageBox.Discard:
                # Don't want to save
                cancel = False
            else:
                # Chose to cancel
                cancel = True
        if cancel:
            return

        if new_plan:
            # Create a new plan
            self.plan = plan.Plan()
            self.copy_plan_to_window()
            self.clear_plan_changed()
        else:
            if path is None:
                # Prompt for plan to load
                # TODO: Set the default loading directory for the dialog to something like the documents folder
                path_str, selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select File"),
                                                                                  None, plan.PLAN_FILE_FILTER)
                if len(path_str) == 0:
                    # Cancel
                    return
                path = pathlib.Path(path_str)

            error_list = []
            loaded_plan = plan.load(path, error_list)
            if loaded_plan is None: # Loading failed
                return

            self.plan = loaded_plan
            self.copy_plan_to_window()
            if self.plan.changed: # If plan was loaded with errors, it will already be marked as changed.
                self.set_plan_changed()     # We call this for its ui update side-effects
            else:
                self.clear_plan_changed()   # We call this for its ui update side-effects

            if len(error_list) > 0:
                self.report_plan_errors(loaded_plan, error_list)
 

    def save_plan(self, prompt_for_path=False):
        # TODO: This method should return a value indicating if saving actually took place or not.

        # If the plan has never been saved/loaded, or its existing file path doesn't exist, we want to prompt
        # to confirm the path. (The path may not exist if the file has been moved/deleted out from under us.)
        if self.plan.new or not self.plan.path.exists():
            prompt_for_path = True

        if prompt_for_path:
            file_path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Select Filename"),
                                                                    str(self.plan.path), plan.PLAN_FILE_FILTER)
            if len(file_path) == 0:
                # Cancel
                return
            self.plan.path = pathlib.Path(file_path)

        self.copy_window_to_plan()
        self.plan.save()
        self.update_read_only_widgets_from_plan()

    def offer_plan_reload(self):
        '''If the current plan was modified due to missing plugins, offer to reload the plan.
        '''
        if self.plan is not None and self.plan._orig_path is not None:
            # The current plan was modified due to missing plugins. Offer to reload
            result = multiscript.app().msg_box(self.tr(f"Would you like to reload the current plan?"),
                        self.tr(f"Reload Plan?"),
                        standard_buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                        default_button=QtWidgets.QMessageBox.Yes)
            if result == QtWidgets.QMessageBox.Yes:
                self.load_plan(self.plan._orig_path)

    #
    # Window update methods
    # 

    def set_plan_changed(self, *args, **kwargs):
        self.plan.changed = True
        self.update_read_only_widgets_from_plan()

    def clear_plan_changed(self, *args, **kwargs):
        self.plan.changed = False
        self.update_read_only_widgets_from_plan()

    def copy_window_to_plan(self):
        self.plan.bible_passages = self.passagesLineEdit.text().strip()
        # We need to save both the versions and the boolean columns in our model. (The boolean
        # columns hold the version checkbox/radio-button selection.)
        # We also want to save these values out in the display order of the rows, rather
        # than than the logical row order stored in the model. That way the display
        # order will become the logical order next time this plan is loaded back in.
        # (For now, we are ignoring the column display order, which will reset each time
        # the application is run.)
        self.plan.bible_versions = self.versionTable.get_items_in_display_order()
        self.plan.version_selection = []
        for model_version_column in self.get_all_version_columns():
            plan_version_column = []
            
            for row_index in self.versionTable.get_item_indexes_in_display_order():
                plan_version_column.append(model_version_column.bool_values[row_index])
            
            self.plan.version_selection.append(plan_version_column)

    def copy_plan_to_window(self):
        self.update_read_only_widgets_from_plan()

        if self.plan.bible_passages is None:
            self.passagesLineEdit.setText("")
        else:
            self.passagesLineEdit.setText(self.plan.bible_passages)

        self.versionModel.clear_items()
        if self.plan.bible_versions is not None:
            self.versionModel.append_items(self.plan.bible_versions)

        # Setting up version columns requires removing existing columns and then adding
        # columns from the plan. We need to preserve the plan-changed state by saving
        # and restoring it (as column changes otherwise for it to set-changed).
        plan_changed = self.plan.changed
        self.remove_all_version_columns()
        if self.plan.version_selection is not None:
            for plan_version_column in self.plan.version_selection:
                model_version_column = self.add_version_column()
                for row_index in range(len(plan_version_column)):
                    model_version_column.bool_values[row_index] = plan_version_column[row_index]
        if plan_changed:
            self.set_plan_changed()
        else:
            self.clear_plan_changed()
        if len(self.get_all_version_columns()) == 0:
            # Ensure there's at least one version column
            self.add_version_column()
        self.versionTable.refresh(resize_cols=True)

    def update_read_only_widgets_from_plan(self):
        # We include the "[*]" placeholder for displaying an asterisk on Windows/Linux when plan is modified.
        self.setWindowTitle(self.plan.path.stem + "[*]")
        self.setWindowModified(self.plan.changed)

        self.planNotesTextEdit.setMarkdown(self.plan.notes)
        self.rowSummaryLabel.setText(self.tr("{0} version(s) in the set".format(self.versionModel.rowCount())))
        self.columnSummaryLabel.setText(self.tr("{0} version(s) per Bible passage".format(
                                        len(self.get_all_version_columns()))))

        template_path = self.plan.template_path
        self.templatePathLabel.setText(template_path.name)
        self.templatePathLabel.setToolTip(str(template_path))
        self.templateIconLabel.setFileIconFromPath(template_path)
        self.templateIconLabel.setToolTip(str(template_path))

        output_dir_path = self.plan.output_dir_path
        self.outputDirPathLabel.setText(output_dir_path.name)
        self.outputDirPathLabel.setToolTip(str(output_dir_path))
        self.outputDirIconLabel.setFileIconFromPath(output_dir_path)
        self.outputDirIconLabel.setToolTip(str(output_dir_path))

    #
    # Information Dialogs
    #

    def check_for_save(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(self.tr("Save changes?"))
        msg_box.setText(self.tr("This plan has been modified."))
        msg_box.setInformativeText(self.tr("Do you wish to save your changes?"))
        msg_box.setIconPixmap(self.windowIcon().pixmap(64, 64))
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.Save)
        return msg_box.exec()

    def report_plan_errors(self, plan, error_list):
        if plan is None:
            msg_text = self.tr("Unfortunately the selected plan could not be loaded.")
        else:
            msg_text = self.tr("The plan was loaded but there were some errors.")
            if plan.changed:
                msg_text += self.tr(" The modified plan has been renamed.")
        
        details_text = "\n\n".join([str(err) for err in error_list])
        plan_errors_dialog = PlanErrorsDialog(None)
        plan_errors_dialog.setMessageText(msg_text)
        plan_errors_dialog.setDetailsText(details_text)
        return plan_errors_dialog.exec()


    #
    # File Menu methods
    #

    def on_new_triggered(self):
        self.load_plan(path=None, new_plan=True)

    def on_open_triggered(self):
        self.load_plan(path=None)

    def on_save_triggered(self):
        self.save_plan()

    def on_save_as_triggered(self):
        self.save_plan(prompt_for_path=True)

    def on_restart_triggered(self):
        multiscript.app().request_restart()

    def closeEvent(self, event):
        if(self.plan.changed):
            result = self.check_for_save()
            if result == QtWidgets.QMessageBox.Save:
                self.save_plan()
                event.accept()
            elif result == QtWidgets.QMessageBox.Discard:
                # Close without saving
                event.accept()
            else:
                # Cancel closing, including cancelling any pending restart
                multiscript.app().restart_requested = False
                event.ignore()
        else:
            event.accept()            

    #
    # Edit Menu methods
    #

    def on_undo_triggered(self):
        focus_widget = QtWidgets.QApplication.focusWidget()
        if focus_widget is not None:
            try:
                focus_widget.undo()
            except AttributeError:
                pass

    def on_redo_triggered(self):
        focus_widget = QtWidgets.QApplication.focusWidget()
        if focus_widget is not None:
            try:
                focus_widget.redo()
            except AttributeError:
                pass

    def on_cut_triggered(self):
        focus_widget = QtWidgets.QApplication.focusWidget()
        if focus_widget is not None:
            try:
                focus_widget.cut()
            except AttributeError:
                pass

    def on_copy_triggered(self):
        focus_widget = QtWidgets.QApplication.focusWidget()
        if focus_widget is not None:
            try:
                focus_widget.copy()
            except AttributeError:
                pass

    def on_paste_triggered(self):
        focus_widget = QtWidgets.QApplication.focusWidget()
        if focus_widget is not None:
            try:
                focus_widget.paste()
            except AttributeError:
                pass

    def on_clear_triggered(self):
        focus_widget = QtWidgets.QApplication.focusWidget()
        if focus_widget is not None:
            try:
                focus_widget.clear()
            except AttributeError:
                pass

    def on_select_all_triggered(self):
        focus_widget = QtWidgets.QApplication.focusWidget()
        if focus_widget is not None:
            try:
                focus_widget.selectAll()
            except AttributeError:
                pass

    def on_plan_config_triggered(self):
        plan_config_dialog = PlanConfigDialog(None, self.plan)
        result = plan_config_dialog.exec()
        if result == QtWidgets.QDialog.Accepted:
            self.set_plan_changed()

    def on_app_config_triggered(self):
        app_config_group = multiscript.app().app_config_group
        app_config_dialog = AppConfigDialog(None, app_config_group)
        # Record existing list of plugins and paths, to detect any changes
        plugins_before = set(multiscript.app().all_plugins)
        plugins_altpath_before = app_config_group.plugins.altPluginsPath
        
        result = app_config_dialog.exec()
        if result == QtWidgets.QDialog.Accepted:
            app_config_group.save()
        
        plugins_after = set(multiscript.app().all_plugins)
        plugins_altpath_after = app_config_group.plugins.altPluginsPath
        if (plugins_altpath_before != plugins_altpath_after) and not multiscript.app().restart_requested:
            result = multiscript.app().msg_box(self.tr(f"The Alternate Plugins Folder has changed. " +
                        f"Would you like to restart Multiscript to process the changes?"),
                        self.tr(f"Restart Multiscript?"),
                        standard_buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                        default_button=QtWidgets.QMessageBox.Yes)
            if result == QtWidgets.QMessageBox.Yes:
                multiscript.app().request_restart()

        if (plugins_before != plugins_after) and not multiscript.app().restart_requested:
            self.offer_plan_reload()

    #
    # Help Menu methods
    #

    def on_about_triggered(self):
        about_dialog = AboutDialog(None)
        about_dialog.exec()






