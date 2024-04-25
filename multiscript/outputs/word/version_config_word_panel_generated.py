# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version_config_word_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_WordVersionConfigPanel(object):
    def setupUi(self, WordVersionConfigPanel):
        if not WordVersionConfigPanel.objectName():
            WordVersionConfigPanel.setObjectName(u"WordVersionConfigPanel")
        WordVersionConfigPanel.resize(215, 55)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WordVersionConfigPanel.sizePolicy().hasHeightForWidth())
        WordVersionConfigPanel.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(WordVersionConfigPanel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.fontSizeLineEdit = QLineEdit(WordVersionConfigPanel)
        self.fontSizeLineEdit.setObjectName(u"fontSizeLineEdit")

        self.gridLayout.addWidget(self.fontSizeLineEdit, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.fontSizeLabel = QLabel(WordVersionConfigPanel)
        self.fontSizeLabel.setObjectName(u"fontSizeLabel")
        sizePolicy.setHeightForWidth(self.fontSizeLabel.sizePolicy().hasHeightForWidth())
        self.fontSizeLabel.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.fontSizeLabel, 1, 0, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(WordVersionConfigPanel)

        QMetaObject.connectSlotsByName(WordVersionConfigPanel)
    # setupUi

    def retranslateUi(self, WordVersionConfigPanel):
        WordVersionConfigPanel.setWindowTitle(QCoreApplication.translate("WordVersionConfigPanel", u"Form", None))
        self.fontSizeLabel.setText(QCoreApplication.translate("WordVersionConfigPanel", u"Font Size", None))
    # retranslateUi

