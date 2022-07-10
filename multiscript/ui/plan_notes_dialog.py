
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from multiscript.ui.plan_notes_dialog_generated import Ui_PlanNotesDialog


class PlanNotesDialog(QtWidgets.QDialog, Ui_PlanNotesDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self.plainNotesTextEdit.textChanged.connect(self.update_notes_view)

    def setNotes(self, notes):
        self.plainNotesTextEdit.setPlainText(notes)
        if len(notes) == 0:
            self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.editPlanNotesWidget))
        else:
            self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.viewPlanNotesWidget))

    def getNotes(self):
        return self.plainNotesTextEdit.toPlainText()
    
    def update_notes_view(self):
        self.richNotesTextEdit.setMarkdown(self.plainNotesTextEdit.toPlainText())
    
    

