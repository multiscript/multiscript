
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from multiscript.ui.plan_errors_dialog_generated import Ui_PlanErrorsDialog


class PlanErrorsDialog(QtWidgets.QDialog, Ui_PlanErrorsDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self.iconLabel.setIcon(self.windowIcon())
    
    def setMessageText(self, text):
        self.messageLabel.setText(text)

    def setDetailsText(self, text):
        self.detailsTextEdit.setPlainText(text)

