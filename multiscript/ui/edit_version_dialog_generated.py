# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_version_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from multiscript.ui.version_form import VersionForm


class Ui_EditVersionDialog(object):
    def setupUi(self, EditVersionDialog):
        if not EditVersionDialog.objectName():
            EditVersionDialog.setObjectName(u"EditVersionDialog")
        EditVersionDialog.resize(363, 533)
        self.verticalLayout = QVBoxLayout(EditVersionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.versionForm = VersionForm(EditVersionDialog)
        self.versionForm.setObjectName(u"versionForm")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionForm.sizePolicy().hasHeightForWidth())
        self.versionForm.setSizePolicy(sizePolicy)
        self.versionForm.setMinimumSize(QSize(370, 469))

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

