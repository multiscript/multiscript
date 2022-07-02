# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plain_text_plan_config_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_PlainTextPlanConfigPanel(object):
    def setupUi(self, PlainTextPlanConfigPanel):
        if not PlainTextPlanConfigPanel.objectName():
            PlainTextPlanConfigPanel.setObjectName(u"PlainTextPlanConfigPanel")
        PlainTextPlanConfigPanel.resize(294, 199)
        self.verticalLayout = QVBoxLayout(PlainTextPlanConfigPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.joinPassageTextLabel = QLabel(PlainTextPlanConfigPanel)
        self.joinPassageTextLabel.setObjectName(u"joinPassageTextLabel")

        self.horizontalLayout.addWidget(self.joinPassageTextLabel)

        self.joinPassageLineEdit = QLineEdit(PlainTextPlanConfigPanel)
        self.joinPassageLineEdit.setObjectName(u"joinPassageLineEdit")

        self.horizontalLayout.addWidget(self.joinPassageLineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabTextLabel = QLabel(PlainTextPlanConfigPanel)
        self.tabTextLabel.setObjectName(u"tabTextLabel")

        self.horizontalLayout_2.addWidget(self.tabTextLabel)

        self.tabTextLineEdit = QLineEdit(PlainTextPlanConfigPanel)
        self.tabTextLineEdit.setObjectName(u"tabTextLineEdit")
        self.tabTextLineEdit.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_2.addWidget(self.tabTextLineEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.afterParaLabel = QLabel(PlainTextPlanConfigPanel)
        self.afterParaLabel.setObjectName(u"afterParaLabel")

        self.horizontalLayout_3.addWidget(self.afterParaLabel)

        self.afterParaLineEdit = QLineEdit(PlainTextPlanConfigPanel)
        self.afterParaLineEdit.setObjectName(u"afterParaLineEdit")
        self.afterParaLineEdit.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_3.addWidget(self.afterParaLineEdit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.insertParaTabCheckBox = QCheckBox(PlainTextPlanConfigPanel)
        self.insertParaTabCheckBox.setObjectName(u"insertParaTabCheckBox")

        self.verticalLayout.addWidget(self.insertParaTabCheckBox)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(30, -1, -1, -1)
        self.skipInitialParaCheckBox = QCheckBox(PlainTextPlanConfigPanel)
        self.skipInitialParaCheckBox.setObjectName(u"skipInitialParaCheckBox")

        self.horizontalLayout_4.addWidget(self.skipInitialParaCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.usePoetryTabsCheckBox = QCheckBox(PlainTextPlanConfigPanel)
        self.usePoetryTabsCheckBox.setObjectName(u"usePoetryTabsCheckBox")

        self.verticalLayout.addWidget(self.usePoetryTabsCheckBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(PlainTextPlanConfigPanel)

        QMetaObject.connectSlotsByName(PlainTextPlanConfigPanel)
    # setupUi

    def retranslateUi(self, PlainTextPlanConfigPanel):
        PlainTextPlanConfigPanel.setWindowTitle(QCoreApplication.translate("PlainTextPlanConfigPanel", u"Form", None))
        self.joinPassageTextLabel.setText(QCoreApplication.translate("PlainTextPlanConfigPanel", u"Join passages with text:", None))
        self.tabTextLabel.setText(QCoreApplication.translate("PlainTextPlanConfigPanel", u"Use this text for tabs:", None))
        self.afterParaLabel.setText(QCoreApplication.translate("PlainTextPlanConfigPanel", u"Insert text after paragraphs:", None))
        self.insertParaTabCheckBox.setText(QCoreApplication.translate("PlainTextPlanConfigPanel", u"Insert tab at start of each paragraph", None))
        self.skipInitialParaCheckBox.setText(QCoreApplication.translate("PlainTextPlanConfigPanel", u"Skip tab on initial paragraph", None))
        self.usePoetryTabsCheckBox.setText(QCoreApplication.translate("PlainTextPlanConfigPanel", u"Indent poetry lines with a tab", None))
    # retranslateUi

