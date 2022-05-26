# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plan_config_word_panel.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_WordPlanConfigPanel(object):
    def setupUi(self, WordPlanConfigPanel):
        if not WordPlanConfigPanel.objectName():
            WordPlanConfigPanel.setObjectName(u"WordPlanConfigPanel")
        WordPlanConfigPanel.resize(449, 174)
        self.verticalLayout = QVBoxLayout(WordPlanConfigPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.joinPassageTextLabel = QLabel(WordPlanConfigPanel)
        self.joinPassageTextLabel.setObjectName(u"joinPassageTextLabel")

        self.horizontalLayout.addWidget(self.joinPassageTextLabel)

        self.joinPassageLineEdit = QLineEdit(WordPlanConfigPanel)
        self.joinPassageLineEdit.setObjectName(u"joinPassageLineEdit")

        self.horizontalLayout.addWidget(self.joinPassageLineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(WordPlanConfigPanel)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.allTablesGroupBox = QGroupBox(WordPlanConfigPanel)
        self.allTablesGroupBox.setObjectName(u"allTablesGroupBox")
        self.verticalLayout_2 = QVBoxLayout(self.allTablesGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.allTablesInsertBlankParasCheckBox = QCheckBox(self.allTablesGroupBox)
        self.allTablesInsertBlankParasCheckBox.setObjectName(u"allTablesInsertBlankParasCheckBox")

        self.verticalLayout_2.addWidget(self.allTablesInsertBlankParasCheckBox)


        self.verticalLayout.addWidget(self.allTablesGroupBox)

        self.generatePDFCheckBox = QCheckBox(WordPlanConfigPanel)
        self.generatePDFCheckBox.setObjectName(u"generatePDFCheckBox")
        self.generatePDFCheckBox.setEnabled(False)

        self.verticalLayout.addWidget(self.generatePDFCheckBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(WordPlanConfigPanel)

        QMetaObject.connectSlotsByName(WordPlanConfigPanel)
    # setupUi

    def retranslateUi(self, WordPlanConfigPanel):
        WordPlanConfigPanel.setWindowTitle(QCoreApplication.translate("WordPlanConfigPanel", u"Form", None))
        self.joinPassageTextLabel.setText(QCoreApplication.translate("WordPlanConfigPanel", u"Join passages with text:", None))
        self.label.setText("")
        self.allTablesGroupBox.setTitle(QCoreApplication.translate("WordPlanConfigPanel", u"When automatically inserting tables (using [MS_ALL_TABLES] tag):", None))
        self.allTablesInsertBlankParasCheckBox.setText(QCoreApplication.translate("WordPlanConfigPanel", u"Insert blank paragraphs before and after tables", None))
        self.generatePDFCheckBox.setText(QCoreApplication.translate("WordPlanConfigPanel", u"FUTURE: Generate PDF files (requires MS Word to be installed)", None))
    # retranslateUi

