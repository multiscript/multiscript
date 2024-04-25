
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from multiscript.ui.edit_version_dialog_generated import Ui_EditVersionDialog
from multiscript.qt_custom.concurrency import call_nonblock, wait_for_nonblock_threads
from multiscript.qt_custom.models import ItemListTableModel
from multiscript import sources


class EditVersionDialog(QtWidgets.QDialog, Ui_EditVersionDialog):
    def __init__(self, parent, version):
        super().__init__(parent)
        self.setupUi()
        self.versionForm.setSingleItem(version)
        
    def setupUi(self):
        super().setupUi(self)
        self.accepted.connect(self.versionForm.submit)
