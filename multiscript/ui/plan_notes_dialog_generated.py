# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plan_notes_dialog.ui'
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
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_PlanNotesDialog(object):
    def setupUi(self, PlanNotesDialog):
        if not PlanNotesDialog.objectName():
            PlanNotesDialog.setObjectName(u"PlanNotesDialog")
        PlanNotesDialog.resize(527, 372)
        self.verticalLayout = QVBoxLayout(PlanNotesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.planNotesTextEdit = QTextEdit(PlanNotesDialog)
        self.planNotesTextEdit.setObjectName(u"planNotesTextEdit")

        self.verticalLayout.addWidget(self.planNotesTextEdit)

        self.buttonBox = QDialogButtonBox(PlanNotesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PlanNotesDialog)
        self.buttonBox.accepted.connect(PlanNotesDialog.accept)
        self.buttonBox.rejected.connect(PlanNotesDialog.reject)

        QMetaObject.connectSlotsByName(PlanNotesDialog)
    # setupUi

    def retranslateUi(self, PlanNotesDialog):
        PlanNotesDialog.setWindowTitle(QCoreApplication.translate("PlanNotesDialog", u"Edit Plan Description", None))
    # retranslateUi

