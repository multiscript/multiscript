# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plan_config_word_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_WordPlanConfigPanel(object):
    def setupUi(self, WordPlanConfigPanel):
        if not WordPlanConfigPanel.objectName():
            WordPlanConfigPanel.setObjectName(u"WordPlanConfigPanel")
        WordPlanConfigPanel.resize(347, 101)
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

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.allTablesInsertBlankParasCheckBox = QCheckBox(WordPlanConfigPanel)
        self.allTablesInsertBlankParasCheckBox.setObjectName(u"allTablesInsertBlankParasCheckBox")

        self.verticalLayout.addWidget(self.allTablesInsertBlankParasCheckBox)

        self.applyDirectFormattingCheckBox = QCheckBox(WordPlanConfigPanel)
        self.applyDirectFormattingCheckBox.setObjectName(u"applyDirectFormattingCheckBox")

        self.verticalLayout.addWidget(self.applyDirectFormattingCheckBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(WordPlanConfigPanel)

        QMetaObject.connectSlotsByName(WordPlanConfigPanel)
    # setupUi

    def retranslateUi(self, WordPlanConfigPanel):
        WordPlanConfigPanel.setWindowTitle(QCoreApplication.translate("WordPlanConfigPanel", u"Form", None))
        self.joinPassageTextLabel.setText(QCoreApplication.translate("WordPlanConfigPanel", u"Join passages with text:", None))
        self.allTablesInsertBlankParasCheckBox.setText(QCoreApplication.translate("WordPlanConfigPanel", u"Insert blank paragraphs before and after new tables", None))
        self.applyDirectFormattingCheckBox.setText(QCoreApplication.translate("WordPlanConfigPanel", u"Apply formatting directly to text, instead of to styles", None))
    # retranslateUi

