
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt

from multiscript.ui.exception_dialog_generated import Ui_ExceptionDialog


class ExceptionDialog(QtWidgets.QDialog, Ui_ExceptionDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self.iconLabel.setIcon(self.windowIcon())
    
    def setDetailsText(self, text):
        self.detailsTextEdit.setPlainText(text)

