# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plan_config_general_panel.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_GeneralPlanConfigPanel(object):
    def setupUi(self, GeneralPlanConfigPanel):
        if not GeneralPlanConfigPanel.objectName():
            GeneralPlanConfigPanel.setObjectName(u"GeneralPlanConfigPanel")
        GeneralPlanConfigPanel.resize(330, 68)
        self.verticalLayout = QVBoxLayout(GeneralPlanConfigPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.allowConfirmationsCheckBox = QCheckBox(GeneralPlanConfigPanel)
        self.allowConfirmationsCheckBox.setObjectName(u"allowConfirmationsCheckBox")

        self.verticalLayout.addWidget(self.allowConfirmationsCheckBox)

        self.confirmAfterTemplateExpansionCheckBox = QCheckBox(GeneralPlanConfigPanel)
        self.confirmAfterTemplateExpansionCheckBox.setObjectName(u"confirmAfterTemplateExpansionCheckBox")

        self.verticalLayout.addWidget(self.confirmAfterTemplateExpansionCheckBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(GeneralPlanConfigPanel)

        QMetaObject.connectSlotsByName(GeneralPlanConfigPanel)
    # setupUi

    def retranslateUi(self, GeneralPlanConfigPanel):
        GeneralPlanConfigPanel.setWindowTitle(QCoreApplication.translate("GeneralPlanConfigPanel", u"Form", None))
        self.allowConfirmationsCheckBox.setText(QCoreApplication.translate("GeneralPlanConfigPanel", u"Pause for confirmation while running plan", None))
        self.confirmAfterTemplateExpansionCheckBox.setText(QCoreApplication.translate("GeneralPlanConfigPanel", u"Pause for confirmation after template expansion", None))
    # retranslateUi

