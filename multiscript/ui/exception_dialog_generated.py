# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exception_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from multiscript.qt_custom.widgets import IconLabel


class Ui_ExceptionDialog(object):
    def setupUi(self, ExceptionDialog):
        if not ExceptionDialog.objectName():
            ExceptionDialog.setObjectName(u"ExceptionDialog")
        ExceptionDialog.resize(431, 333)
        self.verticalLayout = QVBoxLayout(ExceptionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.iconLabel = IconLabel(ExceptionDialog)
        self.iconLabel.setObjectName(u"iconLabel")
        self.iconLabel.setMinimumSize(QSize(64, 64))

        self.horizontalLayout.addWidget(self.iconLabel)

        self.messageLabel = QLabel(ExceptionDialog)
        self.messageLabel.setObjectName(u"messageLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageLabel.sizePolicy().hasHeightForWidth())
        self.messageLabel.setSizePolicy(sizePolicy)
        self.messageLabel.setWordWrap(True)

        self.horizontalLayout.addWidget(self.messageLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.detailsLabel = QLabel(ExceptionDialog)
        self.detailsLabel.setObjectName(u"detailsLabel")

        self.verticalLayout.addWidget(self.detailsLabel)

        self.detailsTextEdit = QPlainTextEdit(ExceptionDialog)
        self.detailsTextEdit.setObjectName(u"detailsTextEdit")
        self.detailsTextEdit.setReadOnly(True)
        self.detailsTextEdit.setTabStopWidth(20)
        self.detailsTextEdit.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.detailsTextEdit)

        self.buttonBox = QDialogButtonBox(ExceptionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ExceptionDialog)
        self.buttonBox.accepted.connect(ExceptionDialog.accept)
        self.buttonBox.rejected.connect(ExceptionDialog.reject)

        QMetaObject.connectSlotsByName(ExceptionDialog)
    # setupUi

    def retranslateUi(self, ExceptionDialog):
        ExceptionDialog.setWindowTitle(QCoreApplication.translate("ExceptionDialog", u"Unexpected Error", None))
        self.iconLabel.setText(QCoreApplication.translate("ExceptionDialog", u"TextLabel", None))
        self.messageLabel.setText(QCoreApplication.translate("ExceptionDialog", u"We're sorry, but an unexpected error has occurred and Multiscript needs to close.", None))
        self.detailsLabel.setText(QCoreApplication.translate("ExceptionDialog", u"Details:", None))
    # retranslateUi

