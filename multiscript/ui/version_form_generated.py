# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version_form.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QWidget)

class Ui_VersionForm(object):
    def setupUi(self, VersionForm):
        if not VersionForm.objectName():
            VersionForm.setObjectName(u"VersionForm")
        VersionForm.setMinimumSize(QSize(370, 520))
        self.gridLayout = QGridLayout(VersionForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.nativeLangLabel = QLabel(VersionForm)
        self.nativeLangLabel.setObjectName(u"nativeLangLabel")

        self.gridLayout.addWidget(self.nativeLangLabel, 6, 0, 1, 1)

        self.userNameLabel = QLabel(VersionForm)
        self.userNameLabel.setObjectName(u"userNameLabel")

        self.gridLayout.addWidget(self.userNameLabel, 9, 0, 1, 1)

        self.userLangLabel = QLabel(VersionForm)
        self.userLangLabel.setObjectName(u"userLangLabel")

        self.gridLayout.addWidget(self.userLangLabel, 11, 0, 1, 1)

        self.userLangLineEdit = QLineEdit(VersionForm)
        self.userLangLineEdit.setObjectName(u"userLangLineEdit")

        self.gridLayout.addWidget(self.userLangLineEdit, 11, 1, 1, 1)

        self.sourceLineEdit = QLineEdit(VersionForm)
        self.sourceLineEdit.setObjectName(u"sourceLineEdit")
        self.sourceLineEdit.setEnabled(False)

        self.gridLayout.addWidget(self.sourceLineEdit, 0, 1, 1, 1)

        self.notesPlainTextEdit = QPlainTextEdit(VersionForm)
        self.notesPlainTextEdit.setObjectName(u"notesPlainTextEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notesPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.notesPlainTextEdit.setSizePolicy(sizePolicy)
        self.notesPlainTextEdit.setMaximumSize(QSize(16777215, 60))

        self.gridLayout.addWidget(self.notesPlainTextEdit, 12, 1, 2, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 15, 0, 1, 1)

        self.nativeAbbrevLabel = QLabel(VersionForm)
        self.nativeAbbrevLabel.setObjectName(u"nativeAbbrevLabel")

        self.gridLayout.addWidget(self.nativeAbbrevLabel, 5, 0, 1, 1)

        self.pushButton = QPushButton(VersionForm)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 13, 0, 1, 1)

        self.nativeNameLabel = QLabel(VersionForm)
        self.nativeNameLabel.setObjectName(u"nativeNameLabel")

        self.gridLayout.addWidget(self.nativeNameLabel, 4, 0, 1, 1)

        self.sourceLabel = QLabel(VersionForm)
        self.sourceLabel.setObjectName(u"sourceLabel")

        self.gridLayout.addWidget(self.sourceLabel, 0, 0, 1, 1)

        self.nativeSectionLabel = QLabel(VersionForm)
        self.nativeSectionLabel.setObjectName(u"nativeSectionLabel")

        self.gridLayout.addWidget(self.nativeSectionLabel, 2, 1, 1, 1)

        self.idLineEdit = QLineEdit(VersionForm)
        self.idLineEdit.setObjectName(u"idLineEdit")

        self.gridLayout.addWidget(self.idLineEdit, 1, 1, 1, 1)

        self.userSectionLabel = QLabel(VersionForm)
        self.userSectionLabel.setObjectName(u"userSectionLabel")

        self.gridLayout.addWidget(self.userSectionLabel, 8, 1, 1, 1)

        self.userAbbrevLabel = QLabel(VersionForm)
        self.userAbbrevLabel.setObjectName(u"userAbbrevLabel")

        self.gridLayout.addWidget(self.userAbbrevLabel, 10, 0, 1, 1)

        self.nativeNameLineEdit = QLineEdit(VersionForm)
        self.nativeNameLineEdit.setObjectName(u"nativeNameLineEdit")

        self.gridLayout.addWidget(self.nativeNameLineEdit, 4, 1, 1, 1)

        self.outputsTabWidget = QTabWidget(VersionForm)
        self.outputsTabWidget.setObjectName(u"outputsTabWidget")

        self.gridLayout.addWidget(self.outputsTabWidget, 14, 0, 1, 2)

        self.userAbbrevLineEdit = QLineEdit(VersionForm)
        self.userAbbrevLineEdit.setObjectName(u"userAbbrevLineEdit")

        self.gridLayout.addWidget(self.userAbbrevLineEdit, 10, 1, 1, 1)

        self.nativeLangLineEdit = QLineEdit(VersionForm)
        self.nativeLangLineEdit.setObjectName(u"nativeLangLineEdit")

        self.gridLayout.addWidget(self.nativeLangLineEdit, 6, 1, 1, 1)

        self.nativeAbbrevLineEdit = QLineEdit(VersionForm)
        self.nativeAbbrevLineEdit.setObjectName(u"nativeAbbrevLineEdit")

        self.gridLayout.addWidget(self.nativeAbbrevLineEdit, 5, 1, 1, 1)

        self.userNameLineEdit = QLineEdit(VersionForm)
        self.userNameLineEdit.setObjectName(u"userNameLineEdit")

        self.gridLayout.addWidget(self.userNameLineEdit, 9, 1, 1, 1)

        self.idLabel = QLabel(VersionForm)
        self.idLabel.setObjectName(u"idLabel")

        self.gridLayout.addWidget(self.idLabel, 1, 0, 1, 1)

        self.notesLabel = QLabel(VersionForm)
        self.notesLabel.setObjectName(u"notesLabel")
        self.notesLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.notesLabel, 12, 0, 1, 1)

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
        self.nativeLangLabel.setText(QCoreApplication.translate("VersionForm", u"Language", None))
        self.userNameLabel.setText(QCoreApplication.translate("VersionForm", u"Version Name", None))
        self.userLangLabel.setText(QCoreApplication.translate("VersionForm", u"Language", None))
        self.nativeAbbrevLabel.setText(QCoreApplication.translate("VersionForm", u"Abbreviation", None))
        self.pushButton.setText(QCoreApplication.translate("VersionForm", u"More...", None))
        self.nativeNameLabel.setText(QCoreApplication.translate("VersionForm", u"Version Name", None))
        self.sourceLabel.setText(QCoreApplication.translate("VersionForm", u"Source", None))
        self.nativeSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Labels in Native Language", None))
        self.userSectionLabel.setText(QCoreApplication.translate("VersionForm", u"Labels in User Language", None))
        self.userAbbrevLabel.setText(QCoreApplication.translate("VersionForm", u"Abbreviation", None))
        self.idLabel.setText(QCoreApplication.translate("VersionForm", u"Version ID", None))
        self.notesLabel.setText(QCoreApplication.translate("VersionForm", u"Notes", None))
    # retranslateUi

