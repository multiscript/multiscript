# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_config_plugins_panel.ui'
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

from multiscript.qt_custom.views import ItemListTableView
from multiscript.qt_custom.widgets import IconLabel


class Ui_PluginsAppConfigPanel(object):
    def setupUi(self, PluginsAppConfigPanel):
        if not PluginsAppConfigPanel.objectName():
            PluginsAppConfigPanel.setObjectName(u"PluginsAppConfigPanel")
        PluginsAppConfigPanel.resize(486, 329)
        self.verticalLayout = QVBoxLayout(PluginsAppConfigPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.pluginsTableView = ItemListTableView(PluginsAppConfigPanel)
        self.pluginsTableView.setObjectName(u"pluginsTableView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.pluginsTableView.sizePolicy().hasHeightForWidth())
        self.pluginsTableView.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pluginsTableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addPluginButton = QPushButton(PluginsAppConfigPanel)
        self.addPluginButton.setObjectName(u"addPluginButton")

        self.horizontalLayout.addWidget(self.addPluginButton)

        self.removePluginButton = QPushButton(PluginsAppConfigPanel)
        self.removePluginButton.setObjectName(u"removePluginButton")

        self.horizontalLayout.addWidget(self.removePluginButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.altPluginsLabel = QLabel(PluginsAppConfigPanel)
        self.altPluginsLabel.setObjectName(u"altPluginsLabel")

        self.verticalLayout.addWidget(self.altPluginsLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.altPluginsPathSelectButton = QPushButton(PluginsAppConfigPanel)
        self.altPluginsPathSelectButton.setObjectName(u"altPluginsPathSelectButton")

        self.horizontalLayout_2.addWidget(self.altPluginsPathSelectButton)

        self.altPluginsPathShowButton = QPushButton(PluginsAppConfigPanel)
        self.altPluginsPathShowButton.setObjectName(u"altPluginsPathShowButton")

        self.horizontalLayout_2.addWidget(self.altPluginsPathShowButton)

        self.altPluginsPathClearButton = QPushButton(PluginsAppConfigPanel)
        self.altPluginsPathClearButton.setObjectName(u"altPluginsPathClearButton")

        self.horizontalLayout_2.addWidget(self.altPluginsPathClearButton)

        self.altPluginsPathIconLabel = IconLabel(PluginsAppConfigPanel)
        self.altPluginsPathIconLabel.setObjectName(u"altPluginsPathIconLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.altPluginsPathIconLabel.sizePolicy().hasHeightForWidth())
        self.altPluginsPathIconLabel.setSizePolicy(sizePolicy1)
        self.altPluginsPathIconLabel.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.altPluginsPathIconLabel)

        self.altPluginsPathLabel = QLabel(PluginsAppConfigPanel)
        self.altPluginsPathLabel.setObjectName(u"altPluginsPathLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.altPluginsPathLabel.sizePolicy().hasHeightForWidth())
        self.altPluginsPathLabel.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.altPluginsPathLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(PluginsAppConfigPanel)

        QMetaObject.connectSlotsByName(PluginsAppConfigPanel)
    # setupUi

    def retranslateUi(self, PluginsAppConfigPanel):
        PluginsAppConfigPanel.setWindowTitle(QCoreApplication.translate("PluginsAppConfigPanel", u"Form", None))
        self.addPluginButton.setText(QCoreApplication.translate("PluginsAppConfigPanel", u"Add...", None))
        self.removePluginButton.setText(QCoreApplication.translate("PluginsAppConfigPanel", u"Remove", None))
        self.altPluginsLabel.setText(QCoreApplication.translate("PluginsAppConfigPanel", u"Alternate Plugins Folder", None))
        self.altPluginsPathSelectButton.setText(QCoreApplication.translate("PluginsAppConfigPanel", u"Select...", None))
        self.altPluginsPathShowButton.setText(QCoreApplication.translate("PluginsAppConfigPanel", u"Show", None))
        self.altPluginsPathClearButton.setText(QCoreApplication.translate("PluginsAppConfigPanel", u"Clear", None))
        self.altPluginsPathIconLabel.setText(QCoreApplication.translate("PluginsAppConfigPanel", u"iconLabel", None))
        self.altPluginsPathLabel.setText(QCoreApplication.translate("PluginsAppConfigPanel", u"TextLabel", None))
    # retranslateUi

