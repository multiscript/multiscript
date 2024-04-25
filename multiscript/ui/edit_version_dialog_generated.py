# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_version_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditVersionDialog.sizePolicy().hasHeightForWidth())
        EditVersionDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(EditVersionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.versionForm = VersionForm(EditVersionDialog)
        self.versionForm.setObjectName(u"versionForm")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.versionForm.sizePolicy().hasHeightForWidth())
        self.versionForm.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.versionForm)

        self.buttonBox = QDialogButtonBox(EditVersionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy2)
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

