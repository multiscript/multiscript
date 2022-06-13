# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        if not ProgressDialog.objectName():
            ProgressDialog.setObjectName(u"ProgressDialog")
        ProgressDialog.resize(600, 396)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProgressDialog.sizePolicy().hasHeightForWidth())
        ProgressDialog.setSizePolicy(sizePolicy)
        ProgressDialog.setMinimumSize(QSize(600, 0))
        ProgressDialog.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.statusLabel = QLabel(ProgressDialog)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setMinimumSize(QSize(0, 32))
        self.statusLabel.setTextFormat(Qt.AutoText)
        self.statusLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.statusLabel)

        self.substatusLabel = QLabel(ProgressDialog)
        self.substatusLabel.setObjectName(u"substatusLabel")

        self.verticalLayout.addWidget(self.substatusLabel)

        self.progressBar = QProgressBar(ProgressDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        self.passagesLabel = QLabel(ProgressDialog)
        self.passagesLabel.setObjectName(u"passagesLabel")

        self.verticalLayout.addWidget(self.passagesLabel)

        self.versionsLabel = QLabel(ProgressDialog)
        self.versionsLabel.setObjectName(u"versionsLabel")

        self.verticalLayout.addWidget(self.versionsLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.showDetailsButton = QPushButton(ProgressDialog)
        self.showDetailsButton.setObjectName(u"showDetailsButton")
        self.showDetailsButton.setCheckable(True)
        self.showDetailsButton.setChecked(False)

        self.horizontalLayout.addWidget(self.showDetailsButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.openButton = QPushButton(ProgressDialog)
        self.openButton.setObjectName(u"openButton")
        self.openButton.setEnabled(False)
        self.openButton.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.openButton)

        self.cancelButton = QPushButton(ProgressDialog)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.cancelButton)

        self.actionButton = QPushButton(ProgressDialog)
        self.actionButton.setObjectName(u"actionButton")
        self.actionButton.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.actionButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.detailsTextEdit = QPlainTextEdit(ProgressDialog)
        self.detailsTextEdit.setObjectName(u"detailsTextEdit")
        self.detailsTextEdit.setEnabled(True)
        self.detailsTextEdit.setReadOnly(True)
        self.detailsTextEdit.setTabStopWidth(20)
        self.detailsTextEdit.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.detailsTextEdit.setBackgroundVisible(False)

        self.verticalLayout.addWidget(self.detailsTextEdit)


        self.retranslateUi(ProgressDialog)

        self.actionButton.setDefault(True)


        QMetaObject.connectSlotsByName(ProgressDialog)
    # setupUi

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(QCoreApplication.translate("ProgressDialog", u"Progress", None))
        self.statusLabel.setText(QCoreApplication.translate("ProgressDialog", u"Status", None))
        self.substatusLabel.setText("")
        self.passagesLabel.setText("")
        self.versionsLabel.setText("")
        self.showDetailsButton.setText(QCoreApplication.translate("ProgressDialog", u"Show Details", None))
        self.openButton.setText(QCoreApplication.translate("ProgressDialog", u"Open", None))
        self.cancelButton.setText(QCoreApplication.translate("ProgressDialog", u"Cancel", None))
        self.actionButton.setText(QCoreApplication.translate("ProgressDialog", u"Action", None))
    # retranslateUi

