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
    QPlainTextEdit, QSizePolicy, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_PlanNotesDialog(object):
    def setupUi(self, PlanNotesDialog):
        if not PlanNotesDialog.objectName():
            PlanNotesDialog.setObjectName(u"PlanNotesDialog")
        PlanNotesDialog.resize(527, 372)
        self.verticalLayout = QVBoxLayout(PlanNotesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(PlanNotesDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.viewPlanNotesWidget = QWidget()
        self.viewPlanNotesWidget.setObjectName(u"viewPlanNotesWidget")
        self.verticalLayout_3 = QVBoxLayout(self.viewPlanNotesWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.richNotesTextEdit = QTextEdit(self.viewPlanNotesWidget)
        self.richNotesTextEdit.setObjectName(u"richNotesTextEdit")
        self.richNotesTextEdit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.richNotesTextEdit)

        self.tabWidget.addTab(self.viewPlanNotesWidget, "")
        self.editPlanNotesWidget = QWidget()
        self.editPlanNotesWidget.setObjectName(u"editPlanNotesWidget")
        self.verticalLayout_2 = QVBoxLayout(self.editPlanNotesWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.plainNotesTextEdit = QPlainTextEdit(self.editPlanNotesWidget)
        self.plainNotesTextEdit.setObjectName(u"plainNotesTextEdit")

        self.verticalLayout_2.addWidget(self.plainNotesTextEdit)

        self.tabWidget.addTab(self.editPlanNotesWidget, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(PlanNotesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PlanNotesDialog)
        self.buttonBox.accepted.connect(PlanNotesDialog.accept)
        self.buttonBox.rejected.connect(PlanNotesDialog.reject)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(PlanNotesDialog)
    # setupUi

    def retranslateUi(self, PlanNotesDialog):
        PlanNotesDialog.setWindowTitle(QCoreApplication.translate("PlanNotesDialog", u"Plan Notes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.viewPlanNotesWidget), QCoreApplication.translate("PlanNotesDialog", u"View Notes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.editPlanNotesWidget), QCoreApplication.translate("PlanNotesDialog", u"Edit Notes - Markdown", None))
    # retranslateUi

