
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from multiscript.ui.version_notes_dialog_generated import Ui_VersionNotesDialog


class VersionNotesDialog(QtWidgets.QDialog, Ui_VersionNotesDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)

    def setNotes(self, notes):
        self.notesPlainTextEdit.setPlainText(notes)

    def getNotes(self):
        return self.notesPlainTextEdit.toPlainText()
