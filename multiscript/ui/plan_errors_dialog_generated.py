# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plan_errors_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
    QHBoxLayout, QLabel, QPlainTextEdit, QSizePolicy,
    QVBoxLayout, QWidget)

from multiscript.qt_custom.widgets import IconLabel

class Ui_PlanErrorsDialog(object):
    def setupUi(self, PlanErrorsDialog):
        if not PlanErrorsDialog.objectName():
            PlanErrorsDialog.setObjectName(u"PlanErrorsDialog")
        PlanErrorsDialog.resize(431, 333)
        self.verticalLayout = QVBoxLayout(PlanErrorsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.iconLabel = IconLabel(PlanErrorsDialog)
        self.iconLabel.setObjectName(u"iconLabel")
        self.iconLabel.setMinimumSize(QSize(64, 64))

        self.horizontalLayout.addWidget(self.iconLabel)

        self.messageLabel = QLabel(PlanErrorsDialog)
        self.messageLabel.setObjectName(u"messageLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageLabel.sizePolicy().hasHeightForWidth())
        self.messageLabel.setSizePolicy(sizePolicy)
        self.messageLabel.setWordWrap(True)

        self.horizontalLayout.addWidget(self.messageLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.detailsLabel = QLabel(PlanErrorsDialog)
        self.detailsLabel.setObjectName(u"detailsLabel")

        self.verticalLayout.addWidget(self.detailsLabel)

        self.detailsTextEdit = QPlainTextEdit(PlanErrorsDialog)
        self.detailsTextEdit.setObjectName(u"detailsTextEdit")
        self.detailsTextEdit.setReadOnly(True)
        self.detailsTextEdit.setTabStopDistance(20.000000000000000)
        self.detailsTextEdit.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.detailsTextEdit)

        self.buttonBox = QDialogButtonBox(PlanErrorsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PlanErrorsDialog)
        self.buttonBox.accepted.connect(PlanErrorsDialog.accept)
        self.buttonBox.rejected.connect(PlanErrorsDialog.reject)

        QMetaObject.connectSlotsByName(PlanErrorsDialog)
    # setupUi

    def retranslateUi(self, PlanErrorsDialog):
        PlanErrorsDialog.setWindowTitle(QCoreApplication.translate("PlanErrorsDialog", u"Plan Errors", None))
        self.iconLabel.setText(QCoreApplication.translate("PlanErrorsDialog", u"TextLabel", None))
        self.messageLabel.setText(QCoreApplication.translate("PlanErrorsDialog", u"Message", None))
        self.detailsLabel.setText(QCoreApplication.translate("PlanErrorsDialog", u"Details:", None))
    # retranslateUi

