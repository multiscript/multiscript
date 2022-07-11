# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version_notes_dialog.ui'
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
    QPlainTextEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_VersionNotesDialog(object):
    def setupUi(self, VersionNotesDialog):
        if not VersionNotesDialog.objectName():
            VersionNotesDialog.setObjectName(u"VersionNotesDialog")
        VersionNotesDialog.resize(527, 372)
        self.verticalLayout = QVBoxLayout(VersionNotesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.notesPlainTextEdit = QPlainTextEdit(VersionNotesDialog)
        self.notesPlainTextEdit.setObjectName(u"notesPlainTextEdit")

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
    # retranslateUi

