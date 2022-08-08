
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from multiscript.ui.version_notes_dialog_generated import Ui_VersionNotesDialog


class VersionNotesDialog(QtWidgets.QDialog, Ui_VersionNotesDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self._in_plan_notes_sync = False
        self._programmatic_plan_notes_change = False
        self.toggleSourceButton.clicked.connect(self.on_toggle_source_button_clicked)
        self.notesTextEdit.textChanged.connect(self.on_notes_rich_text_changed)
        self.notesPlainTextEdit.textChanged.connect(self.on_notes_source_text_changed)
        self.update_notes_source_visibility(False)

    def setNotes(self, notes):
        self.notesTextEdit.setMarkdown(notes)

    def getNotes(self):
        return self.notesTextEdit.toMarkdown()

    def on_toggle_source_button_clicked(self, checked=False):
        self.update_notes_source_visibility(self.notesTextEdit.isVisible())

    def update_notes_source_visibility(self, show_source):
        self.notesTextEdit.setVisible(not show_source)
        self.notesPlainTextEdit.setVisible(show_source)
        if show_source:
            self.toggleSourceButton.setText(self.tr("Hide Markdown"))
            self._programmatic_plan_notes_change = True
            self.on_notes_source_text_changed()
            self._programmatic_plan_notes_change = False
        else:
            self.toggleSourceButton.setText(self.tr("Show Markdown"))
            self._programmatic_plan_notes_change = True
            self.on_notes_rich_text_changed()
            self._programmatic_plan_notes_change = False

    def on_notes_source_text_changed(self):
       if not self._in_plan_notes_sync:
            self._in_plan_notes_sync = True
            self._programmatic_plan_notes_change = True
            self.notesTextEdit.setMarkdown(self.notesPlainTextEdit.toPlainText())
            self._programmatic_plan_notes_change = False
            self._in_plan_notes_sync = False
    
    def on_notes_rich_text_changed(self):
        if not self._in_plan_notes_sync:
            self._in_plan_notes_sync = True
            self._programmatic_plan_notes_change = True
            self.notesPlainTextEdit.setPlainText(self.notesTextEdit.toMarkdown())
            self._programmatic_plan_notes_change = False
            self._in_plan_notes_sync = False
