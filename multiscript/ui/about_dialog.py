
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

import multiscript
from multiscript.ui.about_dialog_generated import Ui_AboutDialog


class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self.appIconLabel.setIcon(multiscript.app().icon)
        self.appVersionLabel.setText(self.tr("Version ") + str(multiscript.get_app_version()))
        self.attributionBrowser.setHtml(multiscript.app().attribution_contents)

    def tr(self, str):
        return QtWidgets.QApplication.translate(self.__class__.__name__, str, None, -1)
