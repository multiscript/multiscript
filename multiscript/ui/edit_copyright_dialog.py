
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from multiscript.ui.edit_copyright_dialog_generated import Ui_EditCopyrightDialog


class EditCopyrightDialog(QtWidgets.QDialog, Ui_EditCopyrightDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)

    def setCopyright(self, copyright):
        self.copyrightTextEdit.setPlainText(copyright)

    def getCopyright(self):
        return self.copyrightTextEdit.toPlainText()
