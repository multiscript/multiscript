# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_copyright_dialog.ui'
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
    QLabel, QPlainTextEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_EditCopyrightDialog(object):
    def setupUi(self, EditCopyrightDialog):
        if not EditCopyrightDialog.objectName():
            EditCopyrightDialog.setObjectName(u"EditCopyrightDialog")
        EditCopyrightDialog.resize(412, 297)
        self.verticalLayout = QVBoxLayout(EditCopyrightDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(EditCopyrightDialog)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.copyrightTextEdit = QPlainTextEdit(EditCopyrightDialog)
        self.copyrightTextEdit.setObjectName(u"copyrightTextEdit")

        self.verticalLayout.addWidget(self.copyrightTextEdit)

        self.buttonBox = QDialogButtonBox(EditCopyrightDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(EditCopyrightDialog)
        self.buttonBox.accepted.connect(EditCopyrightDialog.accept)
        self.buttonBox.rejected.connect(EditCopyrightDialog.reject)

        QMetaObject.connectSlotsByName(EditCopyrightDialog)
    # setupUi

    def retranslateUi(self, EditCopyrightDialog):
        EditCopyrightDialog.setWindowTitle(QCoreApplication.translate("EditCopyrightDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("EditCopyrightDialog", u"Warning: Don't change the copyright text without understanding the legal implications.", None))
    # retranslateUi

