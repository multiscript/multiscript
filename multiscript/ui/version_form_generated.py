# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version_form.ui'
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
from PySide6.QtWidgets import (QApplication, QFontComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTextEdit, QWidget)

class Ui_VersionForm(object):
    def setupUi(self, VersionForm):
        if not VersionForm.objectName():
            VersionForm.setObjectName(u"VersionForm")
        VersionForm.resize(370, 616)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VersionForm.sizePolicy().hasHeightForWidth())
        VersionForm.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(VersionForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.userAbbrevLabel = QLabel(VersionForm)
        self.userAbbrevLabel.setObjectName(u"userAbbrevLabel")

        self.gridLayout.addWidget(self.userAbbrevLabel, 10, 0, 1, 1)

        self.nativeLangLineEdit = QLineEdit(VersionForm)
        self.nativeLangLineEdit.setObjectName(u"nativeLangLineEdit")

        self.gridLayout.addWidget(self.nativeLangLineEdit, 6, 1, 1, 1)

        self.userLangLabel = QLabel(VersionForm)
        self.userLangLabel.setObjectName(u"userLangLabel")

        self.gridLayout.addWidget(self.userLangLabel, 11, 0, 1, 1)

        self.userNameLabel = QLabel(VersionForm)
        self.userNameLabel.setObjectName(u"userNameLabel")

        self.gridLayout.addWidget(self.userNameLabel, 9, 0, 1, 1)

        self.notesLabel = QLabel(VersionForm)
        self.notesLabel.setObjectName(u"notesLabel")
        self.notesLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.notesLabel, 15, 0, 1, 1)

        self.notesTextEdit = QTextEdit(VersionForm)
        self.notesTextEdit.setObjectName(u"notesTextEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.notesTextEdit.sizePolicy().hasHeightForWidth())
        self.notesTextEdit.setSizePolicy(sizePolicy1)
        self.notesTextEdit.setMaximumSize(QSize(16777215, 60))
        self.notesTextEdit.setTabStopDistance(20.000000000000000)

        self.gridLayout.addWidget(self.notesTextEdit, 15, 1, 2, 1)

        self.nativeAbbrevLineEdit = QLineEdit(VersionForm)
        self.nativeAbbrevLineEdit.setObjectName(u"nativeAbbrevLineEdit")

        self.gridLayout.addWidget(self.nativeAbbrevLineEdit, 5, 1, 1, 1)

        self.idLineEdit = QLineEdit(VersionForm)
        self.idLineEdit.setObjectName(u"idLineEdit")

        self.gridLayout.addWidget(self.idLineEdit, 1, 1, 1, 1)

        self.sourceLabel = QLabel(VersionForm)
        self.sourceLabel.setObjectName(u"sourceLabel")

        self.gridLayout.addWidget(self.sourceLabel, 0, 0, 1, 1)

        self.idLabel = QLabel(VersionForm)
        self.idLabel.setObjectName(u"idLabel")

        self.gridLayout.addWidget(self.idLabel, 1, 0, 1, 1)

        self.userSectionLabel = QLabel(VersionForm)
        self.userSectionLabel.setObjectName(u"userSectionLabel")

        self.gridLayout.addWidget(self.userSectionLabel, 8, 1, 1, 1)

        self.nativeLangLabel = QLabel(VersionForm)
        self.nativeLangLabel.setObjectName(u"nativeLangLabel")

        self.gridLayout.addWidget(self.nativeLangLabel, 6, 0, 1, 1)

        self.fontNameFontComboBox = QFontComboBox(VersionForm)
        self.fontNameFontComboBox.setObjectName(u"fontNameFontComboBox")

        self.gridLayout.addWidget(self.fontNameFontComboBox, 13, 1, 1, 1)

        self.outputsTabWidget = QTabWidget(VersionForm)
        self.outputsTabWidget.setObjectName(u"outputsTabWidget")
        sizePolicy.setHeightForWidth(self.outputsTabWidget.sizePolicy().hasHeightForWidth())
        self.outputsTabWidget.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.outputsTabWidget, 17, 0, 1, 2)

        self.userNameLineEdit = QLineEdit(VersionForm)
        self.userNameLineEdit.setObjectName(u"userNameLineEdit")

        self.gridLayout.addWidget(self.userNameLineEdit, 9, 1, 1, 1)

        self.userLangLineEdit = QLineEdit(VersionForm)
        self.userLangLineEdit.setObjectName(u"userLangLineEdit")

        self.gridLayout.addWidget(self.userLangLineEdit, 11, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.moreButton = QPushButton(VersionForm)
        self.moreButton.setObjectName(u"moreButton")

        self.horizontalLayout_3.addWidget(self.moreButton)


        self.gridLayout.addLayout(self.horizontalLayout_3, 16, 0, 1, 1)

        self.fontNameLabel = QLabel(VersionForm)
        self.fontNameLabel.setObjectName(u"fontNameLabel")

        self.gridLayout.addWidget(self.fontNameLabel, 13, 0, 1, 1)

        self.nativeSectionLabel = QLabel(VersionForm)
        self.nativeSectionLabel.setObjectName(u"nativeSectionLabel")

        self.gridLayout.addWidget(self.nativeSectionLabel, 2, 1, 1, 1)

        self.nativeNameLineEdit = QLineEdit(VersionForm)
        self.nativeNameLineEdit.setObjectName(u"nativeNameLineEdit")

        self.gridLayout.addWidget(self.nativeNameLineEdit, 4, 1, 1, 1)

        self.nativeNameLabel = QLabel(VersionForm)
        self.nativeNameLabel.setObjectName(u"nativeNameLabel")

        self.gridLayout.addWidget(self.nativeNameLabel, 4, 0, 1, 1)

        self.fontSizeLineEdit = QLineEdit(VersionForm)
        self.fontSizeLineEdit.setObjectName(u"fontSizeLineEdit")

        self.gridLayout.addWidget(self.fontSizeLineEdit, 14, 1, 1, 1)

        self.userAbbrevLineEdit = QLineEdit(VersionForm)
        self.userAbbrevLineEdit.setObjectName(u"userAbbrevLineEdit")

        self.gridLayout.addWidget(self.userAbbrevLineEdit, 10, 1, 1, 1)

        self.sourceLineEdit = QLineEdit(VersionForm)
        self.sourceLineEdit.setObjectName(u"sourceLineEdit")
        self.sourceLineEdit.setEnabled(False)

        self.gridLayout.addWidget(self.sourceLineEdit, 0, 1, 1, 1)

        self.nativeAbbrevLabel = QLabel(VersionForm)
        self.nativeAbbrevLabel.setObjectName(u"nativeAbbrevLabel")

        self.gridLayout.addWidget(self.nativeAbbrevLabel, 5, 0, 1, 1)

        self.fontSizeLabel = QLabel(VersionForm)
        self.fontSizeLabel.setObjectName(u"fontSizeLabel")

        self.gridLayout.addWidget(self.fontSizeLabel, 14, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 19, 0, 1, 1)

        self.label = QLabel(VersionForm)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 12, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)
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
        self.userLangLabel.setText(QCoreApplication.translate("VersionForm", u"Language", None))
        self.userNameLabel.setText(QCoreApplication.translate("VersionForm", u"Version Name", None))
        self.notesLabel.setText(QCoreApplication.translate("VersionForm", u"Notes", None))
        self.sourceLabel.setText(QCoreApplication.translate("VersionForm", u"Source", None))
        self.idLabel.setText(QCoreApplication.translate("VersionForm", u"Version ID", None))
        self.userSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Labels in User Language", None))
        self.nativeLangLabel.setText(QCoreApplication.translate("VersionForm", u"Language", None))
        self.fontNameFontComboBox.setCurrentText("")
        self.moreButton.setText(QCoreApplication.translate("VersionForm", u"More...", None))
        self.fontNameLabel.setText(QCoreApplication.translate("VersionForm", u"Font Name", None))
        self.nativeSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Labels in Native Language", None))
        self.nativeNameLabel.setText(QCoreApplication.translate("VersionForm", u"Version Name", None))
        self.nativeAbbrevLabel.setText(QCoreApplication.translate("VersionForm", u"Abbreviation", None))
        self.fontSizeLabel.setText(QCoreApplication.translate("VersionForm", u"Font Size", None))
        self.label.setText(QCoreApplication.translate("VersionForm", u"Other Version Details", None))
    # retranslateUi

