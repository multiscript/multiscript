# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plan_config_dialog.ui'
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
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

class Ui_PlanConfigDialog(object):
    def setupUi(self, PlanConfigDialog):
        if not PlanConfigDialog.objectName():
            PlanConfigDialog.setObjectName(u"PlanConfigDialog")
        PlanConfigDialog.resize(597, 388)
        self.verticalLayout = QVBoxLayout(PlanConfigDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.topTabWidget = QTabWidget(PlanConfigDialog)
        self.topTabWidget.setObjectName(u"topTabWidget")
        self.sourcesPage = QWidget()
        self.sourcesPage.setObjectName(u"sourcesPage")
        self.verticalLayout_2 = QVBoxLayout(self.sourcesPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 0)
        self.sourcesTabWidget = QTabWidget(self.sourcesPage)
        self.sourcesTabWidget.setObjectName(u"sourcesTabWidget")

        self.verticalLayout_2.addWidget(self.sourcesTabWidget)

        self.topTabWidget.addTab(self.sourcesPage, "")
        self.outputsPage = QWidget()
        self.outputsPage.setObjectName(u"outputsPage")
        self.verticalLayout_3 = QVBoxLayout(self.outputsPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, -1, 0, 0)
        self.outputsTabWidget = QTabWidget(self.outputsPage)
        self.outputsTabWidget.setObjectName(u"outputsTabWidget")

        self.verticalLayout_3.addWidget(self.outputsTabWidget)

        self.topTabWidget.addTab(self.outputsPage, "")

        self.verticalLayout.addWidget(self.topTabWidget)

        self.buttonBox = QDialogButtonBox(PlanConfigDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PlanConfigDialog)
        self.buttonBox.accepted.connect(PlanConfigDialog.accept)
        self.buttonBox.rejected.connect(PlanConfigDialog.reject)

        self.topTabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(PlanConfigDialog)
    # setupUi

    def retranslateUi(self, PlanConfigDialog):
        PlanConfigDialog.setWindowTitle(QCoreApplication.translate("PlanConfigDialog", u"Plan Options", None))
        self.topTabWidget.setTabText(self.topTabWidget.indexOf(self.sourcesPage), QCoreApplication.translate("PlanConfigDialog", u"Sources", None))
        self.topTabWidget.setTabText(self.topTabWidget.indexOf(self.outputsPage), QCoreApplication.translate("PlanConfigDialog", u"Outputs", None))
    # retranslateUi

