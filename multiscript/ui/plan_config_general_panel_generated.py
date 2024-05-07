# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plan_config_general_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_GeneralPlanConfigPanel(object):
    def setupUi(self, GeneralPlanConfigPanel):
        if not GeneralPlanConfigPanel.objectName():
            GeneralPlanConfigPanel.setObjectName(u"GeneralPlanConfigPanel")
        GeneralPlanConfigPanel.resize(363, 77)
        self.verticalLayout = QVBoxLayout(GeneralPlanConfigPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.allowConfirmationsCheckBox = QCheckBox(GeneralPlanConfigPanel)
        self.allowConfirmationsCheckBox.setObjectName(u"allowConfirmationsCheckBox")

        self.verticalLayout.addWidget(self.allowConfirmationsCheckBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(30, -1, -1, -1)
        self.confirmAfterTemplateExpansionCheckBox = QCheckBox(GeneralPlanConfigPanel)
        self.confirmAfterTemplateExpansionCheckBox.setObjectName(u"confirmAfterTemplateExpansionCheckBox")

        self.horizontalLayout.addWidget(self.confirmAfterTemplateExpansionCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(GeneralPlanConfigPanel)

        QMetaObject.connectSlotsByName(GeneralPlanConfigPanel)
    # setupUi

    def retranslateUi(self, GeneralPlanConfigPanel):
        GeneralPlanConfigPanel.setWindowTitle(QCoreApplication.translate("GeneralPlanConfigPanel", u"Form", None))
        self.allowConfirmationsCheckBox.setText(QCoreApplication.translate("GeneralPlanConfigPanel", u"Pause for confirmation while running plan", None))
        self.confirmAfterTemplateExpansionCheckBox.setText(QCoreApplication.translate("GeneralPlanConfigPanel", u"Pause for confirmation after template expansion", None))
    # retranslateUi

