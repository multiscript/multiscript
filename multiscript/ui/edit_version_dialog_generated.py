# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_version_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QVBoxLayout, QWidget)

from multiscript.ui.version_form import VersionForm

class Ui_EditVersionDialog(object):
    def setupUi(self, EditVersionDialog):
        if not EditVersionDialog.objectName():
            EditVersionDialog.setObjectName(u"EditVersionDialog")
        EditVersionDialog.resize(394, 584)
        self.verticalLayout = QVBoxLayout(EditVersionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.versionForm = VersionForm(EditVersionDialog)
        self.versionForm.setObjectName(u"versionForm")
        self.versionForm.setMinimumSize(QSize(370, 520))

        self.verticalLayout.addWidget(self.versionForm)

        self.buttonBox = QDialogButtonBox(EditVersionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(EditVersionDialog)
        self.buttonBox.accepted.connect(EditVersionDialog.accept)
        self.buttonBox.rejected.connect(EditVersionDialog.reject)

        QMetaObject.connectSlotsByName(EditVersionDialog)
    # setupUi

    def retranslateUi(self, EditVersionDialog):
        EditVersionDialog.setWindowTitle(QCoreApplication.translate("EditVersionDialog", u"Edit Bible Version", None))
    # retranslateUi

