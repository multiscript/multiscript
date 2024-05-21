# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version_notes_dialog.ui'
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
    QHBoxLayout, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_VersionNotesDialog(object):
    def setupUi(self, VersionNotesDialog):
        if not VersionNotesDialog.objectName():
            VersionNotesDialog.setObjectName(u"VersionNotesDialog")
        VersionNotesDialog.resize(527, 372)
        self.verticalLayout = QVBoxLayout(VersionNotesDialog)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.toggleSourceButton = QPushButton(VersionNotesDialog)
        self.toggleSourceButton.setObjectName(u"toggleSourceButton")
        self.toggleSourceButton.setFlat(True)

        self.horizontalLayout.addWidget(self.toggleSourceButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.notesTextEdit = QTextEdit(VersionNotesDialog)
        self.notesTextEdit.setObjectName(u"notesTextEdit")
        self.notesTextEdit.setTabStopDistance(20.000000000000000)

        self.verticalLayout.addWidget(self.notesTextEdit)

        self.notesPlainTextEdit = QPlainTextEdit(VersionNotesDialog)
        self.notesPlainTextEdit.setObjectName(u"notesPlainTextEdit")
        self.notesPlainTextEdit.setTabStopDistance(20.000000000000000)

        self.verticalLayout.addWidget(self.notesPlainTextEdit)

        self.buttonBox = QDialogButtonBox(VersionNotesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(VersionNotesDialog)
        self.buttonBox.accepted.connect(VersionNotesDialog.accept)
        self.buttonBox.rejected.connect(VersionNotesDialog.reject)

        QMetaObject.connectSlotsByName(VersionNotesDialog)
    # setupUi

    def retranslateUi(self, VersionNotesDialog):
        VersionNotesDialog.setWindowTitle(QCoreApplication.translate("VersionNotesDialog", u"Version Notes", None))
        self.toggleSourceButton.setText(QCoreApplication.translate("VersionNotesDialog", u"Show Markdown", None))
    # retranslateUi

