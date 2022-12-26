# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_config_dialog.ui'
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

class Ui_AppConfigDialog(object):
    def setupUi(self, AppConfigDialog):
        if not AppConfigDialog.objectName():
            AppConfigDialog.setObjectName(u"AppConfigDialog")
        AppConfigDialog.resize(597, 388)
        self.verticalLayout = QVBoxLayout(AppConfigDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.topTabWidget = QTabWidget(AppConfigDialog)
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

        self.buttonBox = QDialogButtonBox(AppConfigDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AppConfigDialog)
        self.buttonBox.accepted.connect(AppConfigDialog.accept)
        self.buttonBox.rejected.connect(AppConfigDialog.reject)

        self.topTabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(AppConfigDialog)
    # setupUi

    def retranslateUi(self, AppConfigDialog):
        AppConfigDialog.setWindowTitle(QCoreApplication.translate("AppConfigDialog", u"Settings", None))
        self.topTabWidget.setTabText(self.topTabWidget.indexOf(self.sourcesPage), QCoreApplication.translate("AppConfigDialog", u"Sources", None))
        self.topTabWidget.setTabText(self.topTabWidget.indexOf(self.outputsPage), QCoreApplication.translate("AppConfigDialog", u"Outputs", None))
    # retranslateUi

