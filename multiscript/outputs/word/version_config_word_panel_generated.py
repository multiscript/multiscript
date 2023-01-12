# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version_config_word_panel.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDoubleSpinBox, QFontComboBox,
    QGridLayout, QLabel, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_WordVersionConfigPanel(object):
    def setupUi(self, WordVersionConfigPanel):
        if not WordVersionConfigPanel.objectName():
            WordVersionConfigPanel.setObjectName(u"WordVersionConfigPanel")
        WordVersionConfigPanel.resize(342, 90)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WordVersionConfigPanel.sizePolicy().hasHeightForWidth())
        WordVersionConfigPanel.setSizePolicy(sizePolicy)
        WordVersionConfigPanel.setMinimumSize(QSize(0, 90))
        self.gridLayout = QGridLayout(WordVersionConfigPanel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.fontNameLabel = QLabel(WordVersionConfigPanel)
        self.fontNameLabel.setObjectName(u"fontNameLabel")

        self.gridLayout.addWidget(self.fontNameLabel, 0, 0, 1, 1)

        self.fontSizeDoubleSpinBox = QDoubleSpinBox(WordVersionConfigPanel)
        self.fontSizeDoubleSpinBox.setObjectName(u"fontSizeDoubleSpinBox")
        self.fontSizeDoubleSpinBox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.fontSizeDoubleSpinBox.setDecimals(2)
        self.fontSizeDoubleSpinBox.setMaximum(1000.000000000000000)
        self.fontSizeDoubleSpinBox.setSingleStep(0.250000000000000)

        self.gridLayout.addWidget(self.fontSizeDoubleSpinBox, 2, 1, 1, 1)

        self.fontSizeLabel = QLabel(WordVersionConfigPanel)
        self.fontSizeLabel.setObjectName(u"fontSizeLabel")

        self.gridLayout.addWidget(self.fontSizeLabel, 2, 0, 1, 1)

        self.fontNameFontComboBox = QFontComboBox(WordVersionConfigPanel)
        self.fontNameFontComboBox.setObjectName(u"fontNameFontComboBox")

        self.gridLayout.addWidget(self.fontNameFontComboBox, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 1)


        self.retranslateUi(WordVersionConfigPanel)

        QMetaObject.connectSlotsByName(WordVersionConfigPanel)
    # setupUi

    def retranslateUi(self, WordVersionConfigPanel):
        WordVersionConfigPanel.setWindowTitle(QCoreApplication.translate("WordVersionConfigPanel", u"Form", None))
        self.fontNameLabel.setText(QCoreApplication.translate("WordVersionConfigPanel", u"Font Name", None))
        self.fontSizeDoubleSpinBox.setSpecialValueText(QCoreApplication.translate("WordVersionConfigPanel", u"(0 = Ignore)", None))
        self.fontSizeLabel.setText(QCoreApplication.translate("WordVersionConfigPanel", u"Font Size", None))
        self.fontNameFontComboBox.setCurrentText("")
    # retranslateUi

