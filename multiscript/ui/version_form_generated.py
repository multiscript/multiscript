# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_VersionForm(object):
    def setupUi(self, VersionForm):
        if not VersionForm.objectName():
            VersionForm.setObjectName(u"VersionForm")
        VersionForm.resize(370, 493)
        self.gridLayout = QGridLayout(VersionForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.outputsTabWidget = QTabWidget(VersionForm)
        self.outputsTabWidget.setObjectName(u"outputsTabWidget")

        self.gridLayout.addWidget(self.outputsTabWidget, 13, 0, 1, 2)

        self.userAbbrevLineEdit = QLineEdit(VersionForm)
        self.userAbbrevLineEdit.setObjectName(u"userAbbrevLineEdit")

        self.gridLayout.addWidget(self.userAbbrevLineEdit, 10, 1, 1, 1)

        self.userAbbrevLabel = QLabel(VersionForm)
        self.userAbbrevLabel.setObjectName(u"userAbbrevLabel")

        self.gridLayout.addWidget(self.userAbbrevLabel, 10, 0, 1, 1)

        self.nativeSectionLabel = QLabel(VersionForm)
        self.nativeSectionLabel.setObjectName(u"nativeSectionLabel")

        self.gridLayout.addWidget(self.nativeSectionLabel, 2, 1, 1, 1)

        self.sourceLineEdit = QLineEdit(VersionForm)
        self.sourceLineEdit.setObjectName(u"sourceLineEdit")
        self.sourceLineEdit.setEnabled(False)

        self.gridLayout.addWidget(self.sourceLineEdit, 0, 1, 1, 1)

        self.nativeAbbrevLabel = QLabel(VersionForm)
        self.nativeAbbrevLabel.setObjectName(u"nativeAbbrevLabel")

        self.gridLayout.addWidget(self.nativeAbbrevLabel, 5, 0, 1, 1)

        self.outputSectionLabel = QLabel(VersionForm)
        self.outputSectionLabel.setObjectName(u"outputSectionLabel")

        self.gridLayout.addWidget(self.outputSectionLabel, 12, 1, 1, 1)

        self.nativeAbbrevLineEdit = QLineEdit(VersionForm)
        self.nativeAbbrevLineEdit.setObjectName(u"nativeAbbrevLineEdit")

        self.gridLayout.addWidget(self.nativeAbbrevLineEdit, 5, 1, 1, 1)

        self.nativeNameLineEdit = QLineEdit(VersionForm)
        self.nativeNameLineEdit.setObjectName(u"nativeNameLineEdit")

        self.gridLayout.addWidget(self.nativeNameLineEdit, 4, 1, 1, 1)

        self.sourceLabel = QLabel(VersionForm)
        self.sourceLabel.setObjectName(u"sourceLabel")

        self.gridLayout.addWidget(self.sourceLabel, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 14, 0, 1, 1)

        self.userLangLineEdit = QLineEdit(VersionForm)
        self.userLangLineEdit.setObjectName(u"userLangLineEdit")

        self.gridLayout.addWidget(self.userLangLineEdit, 11, 1, 1, 1)

        self.userSectionLabel = QLabel(VersionForm)
        self.userSectionLabel.setObjectName(u"userSectionLabel")

        self.gridLayout.addWidget(self.userSectionLabel, 8, 1, 1, 1)

        self.idLineEdit = QLineEdit(VersionForm)
        self.idLineEdit.setObjectName(u"idLineEdit")

        self.gridLayout.addWidget(self.idLineEdit, 1, 1, 1, 1)

        self.idLabel = QLabel(VersionForm)
        self.idLabel.setObjectName(u"idLabel")

        self.gridLayout.addWidget(self.idLabel, 1, 0, 1, 1)

        self.userNameLineEdit = QLineEdit(VersionForm)
        self.userNameLineEdit.setObjectName(u"userNameLineEdit")

        self.gridLayout.addWidget(self.userNameLineEdit, 9, 1, 1, 1)

        self.nativeLangLineEdit = QLineEdit(VersionForm)
        self.nativeLangLineEdit.setObjectName(u"nativeLangLineEdit")

        self.gridLayout.addWidget(self.nativeLangLineEdit, 6, 1, 1, 1)

        self.userNameLabel = QLabel(VersionForm)
        self.userNameLabel.setObjectName(u"userNameLabel")

        self.gridLayout.addWidget(self.userNameLabel, 9, 0, 1, 1)

        self.nativeNameLabel = QLabel(VersionForm)
        self.nativeNameLabel.setObjectName(u"nativeNameLabel")

        self.gridLayout.addWidget(self.nativeNameLabel, 4, 0, 1, 1)

        self.userLangLabel = QLabel(VersionForm)
        self.userLangLabel.setObjectName(u"userLangLabel")

        self.gridLayout.addWidget(self.userLangLabel, 11, 0, 1, 1)

        self.nativeLangLabel = QLabel(VersionForm)
        self.nativeLangLabel.setObjectName(u"nativeLangLabel")

        self.gridLayout.addWidget(self.nativeLangLabel, 6, 0, 1, 1)

        QWidget.setTabOrder(self.sourceLineEdit, self.idLineEdit)
        QWidget.setTabOrder(self.idLineEdit, self.nativeNameLineEdit)
        QWidget.setTabOrder(self.nativeNameLineEdit, self.nativeAbbrevLineEdit)
        QWidget.setTabOrder(self.nativeAbbrevLineEdit, self.nativeLangLineEdit)
        QWidget.setTabOrder(self.nativeLangLineEdit, self.userNameLineEdit)
        QWidget.setTabOrder(self.userNameLineEdit, self.userAbbrevLineEdit)
        QWidget.setTabOrder(self.userAbbrevLineEdit, self.userLangLineEdit)

        self.retranslateUi(VersionForm)

        QMetaObject.connectSlotsByName(VersionForm)
    # setupUi

    def retranslateUi(self, VersionForm):
        VersionForm.setWindowTitle(QCoreApplication.translate("VersionForm", u"Form", None))
        self.userAbbrevLabel.setText(QCoreApplication.translate("VersionForm", u"Abbreviation", None))
        self.nativeSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Labels in Native Language", None))
        self.nativeAbbrevLabel.setText(QCoreApplication.translate("VersionForm", u"Abbreviation", None))
        self.outputSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Output Settings\n"
"", None))
        self.sourceLabel.setText(QCoreApplication.translate("VersionForm", u"Source", None))
        self.userSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Labels in User Language", None))
        self.idLabel.setText(QCoreApplication.translate("VersionForm", u"Version ID", None))
        self.userNameLabel.setText(QCoreApplication.translate("VersionForm", u"Version Name", None))
        self.nativeNameLabel.setText(QCoreApplication.translate("VersionForm", u"Version Name", None))
        self.userLangLabel.setText(QCoreApplication.translate("VersionForm", u"Language", None))
        self.nativeLangLabel.setText(QCoreApplication.translate("VersionForm", u"Language", None))
    # retranslateUi

