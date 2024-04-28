from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

import multiscript
from multiscript.qt_custom.forms import Form
from multiscript.ui.version_form_generated import Ui_VersionForm
from multiscript.ui.version_notes_dialog import VersionNotesDialog
from multiscript.qt_custom.model_columns import AttributeColumn


class VersionForm(Form, Ui_VersionForm):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self.moreButton.clicked.connect(self.edit_version_notes)
        self.autoFontCheckBox.stateChanged.connect(self.autoFontCheckBox_stateChanged)
        self.autoFontCheckBox_stateChanged(self.autoFontCheckBox.checkState().value)

        self.output_version_config_subforms = {}
        for output in multiscript.app().all_outputs:
            output_long_id = output.long_id
            output_version_config = output.new_output_version_config()
            if output_version_config is not None:
                output_version_config_subform = output_version_config.new_config_subform()
                if output_version_config_subform is not None:
                    self.output_version_config_subforms[output_long_id] = output_version_config_subform
                    self.outputsTabWidget.addTab(output_version_config_subform, output.name)

    def add_mappings(self):
        self.add_model_column_and_widget(
                AttributeColumn("Source", lambda version: version.bible_source.name, hide=True),
                self.sourceLineEdit
        )
        self.add_model_column_and_widget(
                AttributeColumn("ID", "id", hide=True),
                self.idLineEdit
        )
        self.add_model_column_and_widget(
                AttributeColumn("Native Version Name", lambda version: version.native_labels.name, 
                                lambda version, value: setattr(version.native_labels, "name", value), hide=True),
                self.nativeNameLineEdit
        )
        self.add_model_column_and_widget(
                AttributeColumn("Native Abbrev", lambda version: version.native_labels.abbrev,
                                lambda version, value: setattr(version.native_labels, "abbrev", value), hide=True),
                self.nativeAbbrevLineEdit
        )
        self.add_model_column_and_widget(
                AttributeColumn("Native Lang", lambda version: version.native_labels.lang,
                                lambda version, value: setattr(version.native_labels, "lang", value), hide=True),
                self.nativeLangLineEdit
        )
        self.add_model_column_and_widget(
                AttributeColumn("User Version Name", lambda version: version.user_labels.name,
                                lambda version, value: setattr(version.user_labels, "name", value), hide=True),
                self.userNameLineEdit
        )
        self.add_model_column_and_widget(
                AttributeColumn("User Abbrev", lambda version: version.user_labels.abbrev,
                                lambda version, value: setattr(version.user_labels, "abbrev", value), hide=True),
                self.userAbbrevLineEdit
        )
        self.add_model_column_and_widget(
                AttributeColumn("User Lang", lambda version: version.user_labels.lang,
                                lambda version, value: setattr(version.user_labels, "lang", value), hide=True),
                self.userLangLineEdit
        )
        self.add_model_column_and_widget(
                AttributeColumn("Notes", lambda version: version.notes,
                                lambda version, value: setattr(version, "notes", value.strip()), hide=False),
                self.notesTextEdit, property_name="markdown"
        )
        self.add_model_column_and_widget(
                AttributeColumn("Auto Choose Font", "auto_font", hide=True),
                self.autoFontCheckBox
        )
        self.add_model_column_and_widget(
                AttributeColumn("Font Family", "font_family", hide=True),
                self.fontFamilyFontComboBox
        )
  
        for output_long_id, output_version_config_subform in self.output_version_config_subforms.items():
            bible_output = multiscript.app().output(output_long_id)
            output_version_config_subform.add_mappings(self, bible_output)        

    def edit_version_notes(self):
        version_notes_dialog = VersionNotesDialog(None)
        version_notes_dialog.setNotes(self.notesTextEdit.toMarkdown())
        result = version_notes_dialog.exec()
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            self.notesTextEdit.setMarkdown(version_notes_dialog.getNotes())

    def autoFontCheckBox_stateChanged(self, state):
        self.fontFamilyLabel.setEnabled(state == Qt.CheckState.Unchecked.value)
        self.fontFamilyFontComboBox.setEnabled(state == Qt.CheckState.Unchecked.value)
