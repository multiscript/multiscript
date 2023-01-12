# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
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
    QHBoxLayout, QLabel, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget)

from multiscript.qt_custom.widgets import IconLabel

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(580, 320)
        self.verticalLayout = QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.appIconLabel = IconLabel(AboutDialog)
        self.appIconLabel.setObjectName(u"appIconLabel")
        self.appIconLabel.setMinimumSize(QSize(64, 64))

        self.horizontalLayout.addWidget(self.appIconLabel)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.appNameLabel = QLabel(AboutDialog)
        self.appNameLabel.setObjectName(u"appNameLabel")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.appNameLabel.setFont(font)

        self.verticalLayout_2.addWidget(self.appNameLabel)

        self.appVersionLabel = QLabel(AboutDialog)
        self.appVersionLabel.setObjectName(u"appVersionLabel")

        self.verticalLayout_2.addWidget(self.appVersionLabel)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.attributionBrowser = QTextBrowser(AboutDialog)
        self.attributionBrowser.setObjectName(u"attributionBrowser")
        font1 = QFont()
        font1.setPointSize(12)
        self.attributionBrowser.setFont(font1)
        self.attributionBrowser.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.attributionBrowser)

        self.buttonBox = QDialogButtonBox(AboutDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About Multiscript", None))
        self.appIconLabel.setText(QCoreApplication.translate("AboutDialog", u"appIconLabel", None))
        self.appNameLabel.setText(QCoreApplication.translate("AboutDialog", u"Multiscript", None))
        self.appVersionLabel.setText(QCoreApplication.translate("AboutDialog", u"appVersionLabel", None))
    # retranslateUi

