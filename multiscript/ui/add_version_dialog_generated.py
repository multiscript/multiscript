# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_version_dialog.ui'
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
from multiscript.ui.version_form import VersionForm


class Ui_AddVersionDialog(object):
    def setupUi(self, AddVersionDialog):
        if not AddVersionDialog.objectName():
            AddVersionDialog.setObjectName(u"AddVersionDialog")
        AddVersionDialog.setWindowModality(Qt.NonModal)
        AddVersionDialog.resize(886, 633)
        self.verticalLayout = QVBoxLayout(AddVersionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(AddVersionDialog)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.searchLabel = QLabel(self.verticalLayoutWidget)
        self.searchLabel.setObjectName(u"searchLabel")

        self.horizontalLayout_2.addWidget(self.searchLabel)

        self.filterLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.filterLineEdit.setObjectName(u"filterLineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.filterLineEdit.sizePolicy().hasHeightForWidth())
        self.filterLineEdit.setSizePolicy(sizePolicy1)
        self.filterLineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.filterLineEdit)

        self.editButton = QPushButton(self.verticalLayoutWidget)
        self.editButton.setObjectName(u"editButton")
        self.editButton.setCheckable(True)
        self.editButton.setFlat(False)

        self.horizontalLayout_2.addWidget(self.editButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.versionTable = ItemListTableView(self.verticalLayoutWidget)
        self.versionTable.setObjectName(u"versionTable")
        self.versionTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.versionTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.versionTable.setSortingEnabled(True)
        self.versionTable.horizontalHeader().setHighlightSections(False)
        self.versionTable.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.versionTable)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.statusLabel = QLabel(self.verticalLayoutWidget)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.statusLabel)

        self.progressBar = QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy3)
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(-1)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.refreshButton = QPushButton(self.verticalLayoutWidget)
        self.refreshButton.setObjectName(u"refreshButton")

        self.horizontalLayout.addWidget(self.refreshButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.sidebarForm = QWidget(self.splitter)
        self.sidebarForm.setObjectName(u"sidebarForm")
        self.sidebarForm.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sidebarForm.sizePolicy().hasHeightForWidth())
        self.sidebarForm.setSizePolicy(sizePolicy4)
        self.sidebarForm.setMinimumSize(QSize(0, 0))
        self.sidebarForm.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.sidebarForm)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.addManualButton = QPushButton(self.sidebarForm)
        self.addManualButton.setObjectName(u"addManualButton")

        self.horizontalLayout_3.addWidget(self.addManualButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.versionForm = VersionForm(self.sidebarForm)
        self.versionForm.setObjectName(u"versionForm")
        self.versionForm.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.versionForm.sizePolicy().hasHeightForWidth())
        self.versionForm.setSizePolicy(sizePolicy4)
        self.versionForm.setMinimumSize(QSize(370, 469))

        self.verticalLayout_3.addWidget(self.versionForm)

        self.splitter.addWidget(self.sidebarForm)

        self.verticalLayout.addWidget(self.splitter)

        self.buttonBox = QDialogButtonBox(AddVersionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddVersionDialog)
        self.buttonBox.accepted.connect(AddVersionDialog.accept)
        self.buttonBox.rejected.connect(AddVersionDialog.reject)

        QMetaObject.connectSlotsByName(AddVersionDialog)
    # setupUi

    def retranslateUi(self, AddVersionDialog):
        AddVersionDialog.setWindowTitle(QCoreApplication.translate("AddVersionDialog", u"Add Bible Versions", None))
        self.searchLabel.setText(QCoreApplication.translate("AddVersionDialog", u"Search", None))
        self.filterLineEdit.setText("")
        self.editButton.setText(QCoreApplication.translate("AddVersionDialog", u"Edit Version...", None))
        self.statusLabel.setText(QCoreApplication.translate("AddVersionDialog", u"Status", None))
        self.refreshButton.setText(QCoreApplication.translate("AddVersionDialog", u"Refresh", None))
        self.addManualButton.setText(QCoreApplication.translate("AddVersionDialog", u"Add Manually", None))
    # retranslateUi

