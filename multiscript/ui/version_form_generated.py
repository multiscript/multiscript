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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFontComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_VersionForm(object):
    def setupUi(self, VersionForm):
        if not VersionForm.objectName():
            VersionForm.setObjectName(u"VersionForm")
        VersionForm.resize(402, 593)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VersionForm.sizePolicy().hasHeightForWidth())
        VersionForm.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(VersionForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.nativeSectionLabel = QLabel(VersionForm)
        self.nativeSectionLabel.setObjectName(u"nativeSectionLabel")

        self.gridLayout.addWidget(self.nativeSectionLabel, 2, 1, 1, 1)

        self.userNameLineEdit = QLineEdit(VersionForm)
        self.userNameLineEdit.setObjectName(u"userNameLineEdit")

        self.gridLayout.addWidget(self.userNameLineEdit, 9, 1, 1, 1)

        self.fontFamilyFontComboBox = QFontComboBox(VersionForm)
        self.fontFamilyFontComboBox.setObjectName(u"fontFamilyFontComboBox")

        self.gridLayout.addWidget(self.fontFamilyFontComboBox, 20, 1, 1, 1)

        self.nativeNameLabel = QLabel(VersionForm)
        self.nativeNameLabel.setObjectName(u"nativeNameLabel")

        self.gridLayout.addWidget(self.nativeNameLabel, 4, 0, 1, 1)

        self.userAbbrevLineEdit = QLineEdit(VersionForm)
        self.userAbbrevLineEdit.setObjectName(u"userAbbrevLineEdit")

        self.gridLayout.addWidget(self.userAbbrevLineEdit, 10, 1, 1, 1)

        self.userLangLineEdit = QLineEdit(VersionForm)
        self.userLangLineEdit.setObjectName(u"userLangLineEdit")

        self.gridLayout.addWidget(self.userLangLineEdit, 11, 1, 1, 1)

        self.idLabel = QLabel(VersionForm)
        self.idLabel.setObjectName(u"idLabel")

        self.gridLayout.addWidget(self.idLabel, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.notesTextEdit = QTextEdit(VersionForm)
        self.notesTextEdit.setObjectName(u"notesTextEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.notesTextEdit.sizePolicy().hasHeightForWidth())
        self.notesTextEdit.setSizePolicy(sizePolicy1)
        self.notesTextEdit.setMaximumSize(QSize(16777215, 60))
        self.notesTextEdit.setTabStopDistance(20.000000000000000)

        self.verticalLayout.addWidget(self.notesTextEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.moreButton = QPushButton(VersionForm)
        self.moreButton.setObjectName(u"moreButton")
        self.moreButton.setFlat(False)

        self.horizontalLayout.addWidget(self.moreButton)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.copyrightButton = QPushButton(VersionForm)
        self.copyrightButton.setObjectName(u"copyrightButton")

        self.horizontalLayout.addWidget(self.copyrightButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 14, 1, 2, 1)

        self.sourceLabel = QLabel(VersionForm)
        self.sourceLabel.setObjectName(u"sourceLabel")

        self.gridLayout.addWidget(self.sourceLabel, 0, 0, 1, 1)

        self.idLineEdit = QLineEdit(VersionForm)
        self.idLineEdit.setObjectName(u"idLineEdit")

        self.gridLayout.addWidget(self.idLineEdit, 1, 1, 1, 1)

        self.sourceLineEdit = QLineEdit(VersionForm)
        self.sourceLineEdit.setObjectName(u"sourceLineEdit")
        self.sourceLineEdit.setEnabled(False)

        self.gridLayout.addWidget(self.sourceLineEdit, 0, 1, 1, 1)

        self.userSectionLabel = QLabel(VersionForm)
        self.userSectionLabel.setObjectName(u"userSectionLabel")

        self.gridLayout.addWidget(self.userSectionLabel, 8, 1, 1, 1)

        self.autoFontCheckBox = QCheckBox(VersionForm)
        self.autoFontCheckBox.setObjectName(u"autoFontCheckBox")

        self.gridLayout.addWidget(self.autoFontCheckBox, 19, 1, 1, 1)

        self.otherDetailsSectionLabel = QLabel(VersionForm)
        self.otherDetailsSectionLabel.setObjectName(u"otherDetailsSectionLabel")

        self.gridLayout.addWidget(self.otherDetailsSectionLabel, 12, 1, 1, 1)

        self.nativeNameLineEdit = QLineEdit(VersionForm)
        self.nativeNameLineEdit.setObjectName(u"nativeNameLineEdit")

        self.gridLayout.addWidget(self.nativeNameLineEdit, 4, 1, 1, 1)

        self.nativeLangLabel = QLabel(VersionForm)
        self.nativeLangLabel.setObjectName(u"nativeLangLabel")

        self.gridLayout.addWidget(self.nativeLangLabel, 6, 0, 1, 1)

        self.userNameLabel = QLabel(VersionForm)
        self.userNameLabel.setObjectName(u"userNameLabel")

        self.gridLayout.addWidget(self.userNameLabel, 9, 0, 1, 1)

        self.userLangLabel = QLabel(VersionForm)
        self.userLangLabel.setObjectName(u"userLangLabel")

        self.gridLayout.addWidget(self.userLangLabel, 11, 0, 1, 1)

        self.outputsTabWidget = QTabWidget(VersionForm)
        self.outputsTabWidget.setObjectName(u"outputsTabWidget")
        sizePolicy.setHeightForWidth(self.outputsTabWidget.sizePolicy().hasHeightForWidth())
        self.outputsTabWidget.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.outputsTabWidget, 22, 0, 1, 2)

        self.userAbbrevLabel = QLabel(VersionForm)
        self.userAbbrevLabel.setObjectName(u"userAbbrevLabel")

        self.gridLayout.addWidget(self.userAbbrevLabel, 10, 0, 1, 1)

        self.fontFamilyLabel = QLabel(VersionForm)
        self.fontFamilyLabel.setObjectName(u"fontFamilyLabel")

        self.gridLayout.addWidget(self.fontFamilyLabel, 20, 0, 1, 1)

        self.nativeLangLineEdit = QLineEdit(VersionForm)
        self.nativeLangLineEdit.setObjectName(u"nativeLangLineEdit")

        self.gridLayout.addWidget(self.nativeLangLineEdit, 6, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 24, 0, 1, 1)

        self.nativeAbbrevLabel = QLabel(VersionForm)
        self.nativeAbbrevLabel.setObjectName(u"nativeAbbrevLabel")

        self.gridLayout.addWidget(self.nativeAbbrevLabel, 5, 0, 1, 1)

        self.notesLabel = QLabel(VersionForm)
        self.notesLabel.setObjectName(u"notesLabel")
        self.notesLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.notesLabel, 14, 0, 1, 1)

        self.nativeAbbrevLineEdit = QLineEdit(VersionForm)
        self.nativeAbbrevLineEdit.setObjectName(u"nativeAbbrevLineEdit")

        self.gridLayout.addWidget(self.nativeAbbrevLineEdit, 5, 1, 1, 1)

        self.isRTLCheckBox = QCheckBox(VersionForm)
        self.isRTLCheckBox.setObjectName(u"isRTLCheckBox")

        self.gridLayout.addWidget(self.isRTLCheckBox, 21, 1, 1, 1)

        self.isRTLLabel = QLabel(VersionForm)
        self.isRTLLabel.setObjectName(u"isRTLLabel")

        self.gridLayout.addWidget(self.isRTLLabel, 21, 0, 1, 1)

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
        self.nativeSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Labels \u2013 Native Language", None))
        self.fontFamilyFontComboBox.setCurrentText("")
        self.nativeNameLabel.setText(QCoreApplication.translate("VersionForm", u"Version Name", None))
        self.idLabel.setText(QCoreApplication.translate("VersionForm", u"Version ID", None))
        self.moreButton.setText(QCoreApplication.translate("VersionForm", u"More...", None))
        self.copyrightButton.setText(QCoreApplication.translate("VersionForm", u"Copyright...", None))
        self.sourceLabel.setText(QCoreApplication.translate("VersionForm", u"Source", None))
        self.userSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Labels \u2013 User Language", None))
        self.autoFontCheckBox.setText(QCoreApplication.translate("VersionForm", u"Automatically select font family", None))
        self.otherDetailsSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Other Details", None))
        self.nativeLangLabel.setText(QCoreApplication.translate("VersionForm", u"Language", None))
        self.userNameLabel.setText(QCoreApplication.translate("VersionForm", u"Version Name", None))
        self.userLangLabel.setText(QCoreApplication.translate("VersionForm", u"Language", None))
        self.userAbbrevLabel.setText(QCoreApplication.translate("VersionForm", u"Abbreviation", None))
        self.fontFamilyLabel.setText(QCoreApplication.translate("VersionForm", u"Font Family", None))
        self.nativeAbbrevLabel.setText(QCoreApplication.translate("VersionForm", u"Abbreviation", None))
        self.notesLabel.setText(QCoreApplication.translate("VersionForm", u"Notes", None))
        self.isRTLCheckBox.setText(QCoreApplication.translate("VersionForm", u"Right-to-left", None))
        self.isRTLLabel.setText(QCoreApplication.translate("VersionForm", u"Text Direction", None))
    # retranslateUi

