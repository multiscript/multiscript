# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_config_general_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_GeneralAppConfigPanel(object):
    def setupUi(self, GeneralAppConfigPanel):
        if not GeneralAppConfigPanel.objectName():
            GeneralAppConfigPanel.setObjectName(u"GeneralAppConfigPanel")
        GeneralAppConfigPanel.resize(370, 144)
        self.verticalLayout = QVBoxLayout(GeneralAppConfigPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.savePlansBeforeExecutionCheckBox = QCheckBox(GeneralAppConfigPanel)
        self.savePlansBeforeExecutionCheckBox.setObjectName(u"savePlansBeforeExecutionCheckBox")

        self.verticalLayout.addWidget(self.savePlansBeforeExecutionCheckBox)

        self.keepExistingTemplateFilesCheckBox = QCheckBox(GeneralAppConfigPanel)
        self.keepExistingTemplateFilesCheckBox.setObjectName(u"keepExistingTemplateFilesCheckBox")

        self.verticalLayout.addWidget(self.keepExistingTemplateFilesCheckBox)

        self.keepExistingOutputFilesCheckbox = QCheckBox(GeneralAppConfigPanel)
        self.keepExistingOutputFilesCheckbox.setObjectName(u"keepExistingOutputFilesCheckbox")

        self.verticalLayout.addWidget(self.keepExistingOutputFilesCheckbox)

        self.ignoredScriptsLabel = QLabel(GeneralAppConfigPanel)
        self.ignoredScriptsLabel.setObjectName(u"ignoredScriptsLabel")

        self.verticalLayout.addWidget(self.ignoredScriptsLabel)

        self.ignoredScriptsLineEdit = QLineEdit(GeneralAppConfigPanel)
        self.ignoredScriptsLineEdit.setObjectName(u"ignoredScriptsLineEdit")

        self.verticalLayout.addWidget(self.ignoredScriptsLineEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(GeneralAppConfigPanel)

        QMetaObject.connectSlotsByName(GeneralAppConfigPanel)
    # setupUi

    def retranslateUi(self, GeneralAppConfigPanel):
        GeneralAppConfigPanel.setWindowTitle(QCoreApplication.translate("GeneralAppConfigPanel", u"Form", None))
        self.savePlansBeforeExecutionCheckBox.setText(QCoreApplication.translate("GeneralAppConfigPanel", u"Save plans before executing them", None))
        self.keepExistingTemplateFilesCheckBox.setText(QCoreApplication.translate("GeneralAppConfigPanel", u"Keep existing template files instead of recreating them", None))
        self.keepExistingOutputFilesCheckbox.setText(QCoreApplication.translate("GeneralAppConfigPanel", u"Keep existing output files instead of recreating them", None))
        self.ignoredScriptsLabel.setText(QCoreApplication.translate("GeneralAppConfigPanel", u"Don't automatically select fonts for these Unicode scripts:", None))
    # retranslateUi

