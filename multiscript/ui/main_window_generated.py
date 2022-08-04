# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QTextEdit,
    QVBoxLayout, QWidget)

from multiscript.qt_custom.views import ItemListTableView
from multiscript.qt_custom.widgets import IconLabel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(752, 720)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.openAction = QAction(MainWindow)
        self.openAction.setObjectName(u"openAction")
        self.saveAsAction = QAction(MainWindow)
        self.saveAsAction.setObjectName(u"saveAsAction")
        self.aboutAction = QAction(MainWindow)
        self.aboutAction.setObjectName(u"aboutAction")
        self.aboutAction.setMenuRole(QAction.AboutRole)
        self.appConfigAction = QAction(MainWindow)
        self.appConfigAction.setObjectName(u"appConfigAction")
        self.appConfigAction.setMenuRole(QAction.PreferencesRole)
        self.closeAction = QAction(MainWindow)
        self.closeAction.setObjectName(u"closeAction")
        self.saveAction = QAction(MainWindow)
        self.saveAction.setObjectName(u"saveAction")
        self.newAction = QAction(MainWindow)
        self.newAction.setObjectName(u"newAction")
        self.exitAction = QAction(MainWindow)
        self.exitAction.setObjectName(u"exitAction")
        self.exitAction.setMenuRole(QAction.QuitRole)
        self.undoAction = QAction(MainWindow)
        self.undoAction.setObjectName(u"undoAction")
        self.redoAction = QAction(MainWindow)
        self.redoAction.setObjectName(u"redoAction")
        self.cutAction = QAction(MainWindow)
        self.cutAction.setObjectName(u"cutAction")
        self.copyAction = QAction(MainWindow)
        self.copyAction.setObjectName(u"copyAction")
        self.pasteAction = QAction(MainWindow)
        self.pasteAction.setObjectName(u"pasteAction")
        self.clearAction = QAction(MainWindow)
        self.clearAction.setObjectName(u"clearAction")
        self.selectAllAction = QAction(MainWindow)
        self.selectAllAction.setObjectName(u"selectAllAction")
        self.planConfigAction = QAction(MainWindow)
        self.planConfigAction.setObjectName(u"planConfigAction")
        self.restartAction = QAction(MainWindow)
        self.restartAction.setObjectName(u"restartAction")
        self.restartAction.setVisible(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.mainLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(12, 0, 12, 0)
        self.titleAreaWidget = QWidget(self.verticalLayoutWidget)
        self.titleAreaWidget.setObjectName(u"titleAreaWidget")
        self.titleAreaWidget.setAutoFillBackground(False)
        self.titleAreaWidgetLayout = QVBoxLayout(self.titleAreaWidget)
        self.titleAreaWidgetLayout.setObjectName(u"titleAreaWidgetLayout")
        self.titleAreaWidgetLayout.setContentsMargins(0, 12, 0, 12)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.appIconLabel = IconLabel(self.titleAreaWidget)
        self.appIconLabel.setObjectName(u"appIconLabel")
        self.appIconLabel.setMinimumSize(QSize(64, 64))

        self.horizontalLayout_3.addWidget(self.appIconLabel)

        self.horizontalSpacer_4 = QSpacerItem(6, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.titleLabel = QLabel(self.titleAreaWidget)
        self.titleLabel.setObjectName(u"titleLabel")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.titleLabel.setFont(font)

        self.horizontalLayout_3.addWidget(self.titleLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.togglePlanNotesButton = QPushButton(self.titleAreaWidget)
        self.togglePlanNotesButton.setObjectName(u"togglePlanNotesButton")

        self.verticalLayout.addWidget(self.togglePlanNotesButton)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.verticalLayout)


        self.titleAreaWidgetLayout.addLayout(self.horizontalLayout_3)


        self.mainLayout.addWidget(self.titleAreaWidget)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addWidget(self.line)

        self.mainAreaWidget = QWidget(self.verticalLayoutWidget)
        self.mainAreaWidget.setObjectName(u"mainAreaWidget")
        self.mainAreaWidgetLayout = QVBoxLayout(self.mainAreaWidget)
        self.mainAreaWidgetLayout.setObjectName(u"mainAreaWidgetLayout")
        self.mainAreaWidgetLayout.setContentsMargins(0, 12, 0, 12)
        self.passagesLabel = QLabel(self.mainAreaWidget)
        self.passagesLabel.setObjectName(u"passagesLabel")
        font1 = QFont()
        font1.setBold(True)
        self.passagesLabel.setFont(font1)

        self.mainAreaWidgetLayout.addWidget(self.passagesLabel)

        self.passagesLineEdit = QLineEdit(self.mainAreaWidget)
        self.passagesLineEdit.setObjectName(u"passagesLineEdit")

        self.mainAreaWidgetLayout.addWidget(self.passagesLineEdit)

        self.versionsTableLabel = QLabel(self.mainAreaWidget)
        self.versionsTableLabel.setObjectName(u"versionsTableLabel")
        self.versionsTableLabel.setFont(font1)

        self.mainAreaWidgetLayout.addWidget(self.versionsTableLabel)

        self.versionsVerticalLayout = QVBoxLayout()
        self.versionsVerticalLayout.setObjectName(u"versionsVerticalLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(12)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.addRowsButton = QPushButton(self.mainAreaWidget)
        self.addRowsButton.setObjectName(u"addRowsButton")
        self.addRowsButton.setAutoDefault(True)

        self.horizontalLayout_8.addWidget(self.addRowsButton)

        self.removeRowsButton = QPushButton(self.mainAreaWidget)
        self.removeRowsButton.setObjectName(u"removeRowsButton")
        self.removeRowsButton.setAutoDefault(True)

        self.horizontalLayout_8.addWidget(self.removeRowsButton)

        self.editButton = QPushButton(self.mainAreaWidget)
        self.editButton.setObjectName(u"editButton")
        self.editButton.setAutoDefault(True)

        self.horizontalLayout_8.addWidget(self.editButton)

        self.rowSummaryLabel = QLabel(self.mainAreaWidget)
        self.rowSummaryLabel.setObjectName(u"rowSummaryLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rowSummaryLabel.sizePolicy().hasHeightForWidth())
        self.rowSummaryLabel.setSizePolicy(sizePolicy1)
        self.rowSummaryLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.rowSummaryLabel)


        self.versionsVerticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.versionTable = ItemListTableView(self.mainAreaWidget)
        self.versionTable.setObjectName(u"versionTable")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.versionTable.sizePolicy().hasHeightForWidth())
        self.versionTable.setSizePolicy(sizePolicy2)
        self.versionTable.horizontalHeader().setHighlightSections(False)
        self.versionTable.horizontalHeader().setStretchLastSection(True)
        self.versionTable.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout_12.addWidget(self.versionTable)


        self.versionsVerticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(12)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.addColumnButton = QPushButton(self.mainAreaWidget)
        self.addColumnButton.setObjectName(u"addColumnButton")

        self.horizontalLayout_13.addWidget(self.addColumnButton)

        self.removeColumnButton = QPushButton(self.mainAreaWidget)
        self.removeColumnButton.setObjectName(u"removeColumnButton")

        self.horizontalLayout_13.addWidget(self.removeColumnButton)

        self.columnSummaryLabel = QLabel(self.mainAreaWidget)
        self.columnSummaryLabel.setObjectName(u"columnSummaryLabel")
        sizePolicy1.setHeightForWidth(self.columnSummaryLabel.sizePolicy().hasHeightForWidth())
        self.columnSummaryLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_13.addWidget(self.columnSummaryLabel)


        self.versionsVerticalLayout.addLayout(self.horizontalLayout_13)

        self.versionsVerticalLayout.setStretch(1, 1)

        self.mainAreaWidgetLayout.addLayout(self.versionsVerticalLayout)

        self.pathsLayout = QGridLayout()
        self.pathsLayout.setObjectName(u"pathsLayout")
        self.outputLabel = QLabel(self.mainAreaWidget)
        self.outputLabel.setObjectName(u"outputLabel")
        self.outputLabel.setFont(font1)

        self.pathsLayout.addWidget(self.outputLabel, 0, 1, 1, 1)

        self.templateLabel = QLabel(self.mainAreaWidget)
        self.templateLabel.setObjectName(u"templateLabel")
        self.templateLabel.setFont(font1)

        self.pathsLayout.addWidget(self.templateLabel, 0, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.templateIconLabel = IconLabel(self.mainAreaWidget)
        self.templateIconLabel.setObjectName(u"templateIconLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.templateIconLabel.sizePolicy().hasHeightForWidth())
        self.templateIconLabel.setSizePolicy(sizePolicy3)
        self.templateIconLabel.setMinimumSize(QSize(0, 32))
        self.templateIconLabel.setFrameShape(QFrame.NoFrame)
        self.templateIconLabel.setScaledContents(False)

        self.horizontalLayout_5.addWidget(self.templateIconLabel)

        self.templatePathLabel = QLabel(self.mainAreaWidget)
        self.templatePathLabel.setObjectName(u"templatePathLabel")
        sizePolicy1.setHeightForWidth(self.templatePathLabel.sizePolicy().hasHeightForWidth())
        self.templatePathLabel.setSizePolicy(sizePolicy1)
        self.templatePathLabel.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_5.addWidget(self.templatePathLabel)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.templateSelectButton = QPushButton(self.mainAreaWidget)
        self.templateSelectButton.setObjectName(u"templateSelectButton")
        self.templateSelectButton.setAutoDefault(True)

        self.horizontalLayout_6.addWidget(self.templateSelectButton)

        self.templateShowButton = QPushButton(self.mainAreaWidget)
        self.templateShowButton.setObjectName(u"templateShowButton")

        self.horizontalLayout_6.addWidget(self.templateShowButton)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.pathsLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.outputDirIconLabel = IconLabel(self.mainAreaWidget)
        self.outputDirIconLabel.setObjectName(u"outputDirIconLabel")
        self.outputDirIconLabel.setMinimumSize(QSize(0, 32))

        self.horizontalLayout_4.addWidget(self.outputDirIconLabel)

        self.outputDirPathLabel = QLabel(self.mainAreaWidget)
        self.outputDirPathLabel.setObjectName(u"outputDirPathLabel")
        sizePolicy1.setHeightForWidth(self.outputDirPathLabel.sizePolicy().hasHeightForWidth())
        self.outputDirPathLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.outputDirPathLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.outputDirSelectButton = QPushButton(self.mainAreaWidget)
        self.outputDirSelectButton.setObjectName(u"outputDirSelectButton")
        self.outputDirSelectButton.setAutoDefault(True)

        self.horizontalLayout_7.addWidget(self.outputDirSelectButton)

        self.outputDirShowButton = QPushButton(self.mainAreaWidget)
        self.outputDirShowButton.setObjectName(u"outputDirShowButton")

        self.horizontalLayout_7.addWidget(self.outputDirShowButton)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.pathsLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.pathsLayout.setColumnStretch(0, 1)
        self.pathsLayout.setColumnStretch(1, 1)

        self.mainAreaWidgetLayout.addLayout(self.pathsLayout)


        self.mainLayout.addWidget(self.mainAreaWidget)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addWidget(self.line_2)

        self.footerAreaWidget = QWidget(self.verticalLayoutWidget)
        self.footerAreaWidget.setObjectName(u"footerAreaWidget")
        self.footerLayout = QHBoxLayout(self.footerAreaWidget)
        self.footerLayout.setObjectName(u"footerLayout")
        self.footerLayout.setContentsMargins(0, 12, 0, 18)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footerLayout.addItem(self.horizontalSpacer_2)

        self.closeButton = QPushButton(self.footerAreaWidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setAutoDefault(True)

        self.footerLayout.addWidget(self.closeButton)

        self.planConfigButton = QPushButton(self.footerAreaWidget)
        self.planConfigButton.setObjectName(u"planConfigButton")

        self.footerLayout.addWidget(self.planConfigButton)

        self.startButton = QPushButton(self.footerAreaWidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setAutoDefault(True)

        self.footerLayout.addWidget(self.startButton)


        self.mainLayout.addWidget(self.footerAreaWidget)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.sidePanelLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.sidePanelLayout.setObjectName(u"sidePanelLayout")
        self.sidePanelLayout.setContentsMargins(0, 0, 0, 0)
        self.sidePanelWidget = QWidget(self.verticalLayoutWidget_2)
        self.sidePanelWidget.setObjectName(u"sidePanelWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sidePanelWidget.sizePolicy().hasHeightForWidth())
        self.sidePanelWidget.setSizePolicy(sizePolicy4)
        self.sidePanelWidget.setMinimumSize(QSize(150, 100))
        self.verticalLayout_5 = QVBoxLayout(self.sidePanelWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.toggleSourceButton = QPushButton(self.sidePanelWidget)
        self.toggleSourceButton.setObjectName(u"toggleSourceButton")
        self.toggleSourceButton.setFlat(True)

        self.horizontalLayout.addWidget(self.toggleSourceButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.planNotesTextEdit = QTextEdit(self.sidePanelWidget)
        self.planNotesTextEdit.setObjectName(u"planNotesTextEdit")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.planNotesTextEdit.sizePolicy().hasHeightForWidth())
        self.planNotesTextEdit.setSizePolicy(sizePolicy5)
        self.planNotesTextEdit.setMaximumSize(QSize(16777215, 16777215))
        self.planNotesTextEdit.setReadOnly(True)
        self.planNotesTextEdit.setTabStopDistance(20.000000000000000)
        self.planNotesTextEdit.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_5.addWidget(self.planNotesTextEdit)

        self.planNotesPlainTextEdit = QPlainTextEdit(self.sidePanelWidget)
        self.planNotesPlainTextEdit.setObjectName(u"planNotesPlainTextEdit")

        self.verticalLayout_5.addWidget(self.planNotesPlainTextEdit)


        self.sidePanelLayout.addWidget(self.sidePanelWidget)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_3.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 752, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.newAction)
        self.menuFile.addAction(self.openAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.closeAction)
        self.menuFile.addAction(self.saveAction)
        self.menuFile.addAction(self.saveAsAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.restartAction)
        self.menuFile.addAction(self.exitAction)
        self.menuEdit.addAction(self.undoAction)
        self.menuEdit.addAction(self.redoAction)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.cutAction)
        self.menuEdit.addAction(self.copyAction)
        self.menuEdit.addAction(self.pasteAction)
        self.menuEdit.addAction(self.clearAction)
        self.menuEdit.addAction(self.selectAllAction)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.planConfigAction)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.appConfigAction)
        self.menuHelp.addAction(self.aboutAction)

        self.retranslateUi(MainWindow)

        self.startButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Multiscript", None))
        self.openAction.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
#if QT_CONFIG(shortcut)
        self.openAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.saveAsAction.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
#if QT_CONFIG(shortcut)
        self.saveAsAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.aboutAction.setText(QCoreApplication.translate("MainWindow", u"About Multiscript", None))
        self.appConfigAction.setText(QCoreApplication.translate("MainWindow", u"Multiscript Settings...", None))
        self.closeAction.setText(QCoreApplication.translate("MainWindow", u"Close", None))
#if QT_CONFIG(shortcut)
        self.closeAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.saveAction.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.saveAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.newAction.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.newAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.exitAction.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.undoAction.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
#if QT_CONFIG(shortcut)
        self.undoAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.redoAction.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
#if QT_CONFIG(shortcut)
        self.redoAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Z", None))
#endif // QT_CONFIG(shortcut)
        self.cutAction.setText(QCoreApplication.translate("MainWindow", u"Cut", None))
#if QT_CONFIG(shortcut)
        self.cutAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.copyAction.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
#if QT_CONFIG(shortcut)
        self.copyAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.pasteAction.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
#if QT_CONFIG(shortcut)
        self.pasteAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.clearAction.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.selectAllAction.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
#if QT_CONFIG(shortcut)
        self.selectAllAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.planConfigAction.setText(QCoreApplication.translate("MainWindow", u"Plan Options...", None))
        self.restartAction.setText(QCoreApplication.translate("MainWindow", u"Restart Multiscript", None))
        self.appIconLabel.setText(QCoreApplication.translate("MainWindow", u"IconLabel", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Multiscript", None))
        self.togglePlanNotesButton.setText(QCoreApplication.translate("MainWindow", u"Toggle Plan Notes", None))
        self.passagesLabel.setText(QCoreApplication.translate("MainWindow", u"Bible Passages", None))
        self.passagesLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"For example: Gen 1:1-5, Gen 1:26-27; John 1:1-18, John 2:1-11", None))
        self.versionsTableLabel.setText(QCoreApplication.translate("MainWindow", u"\n"
"Bible Versions", None))
        self.addRowsButton.setText(QCoreApplication.translate("MainWindow", u"Add Versions to Set...", None))
        self.removeRowsButton.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.editButton.setText(QCoreApplication.translate("MainWindow", u"Edit...", None))
        self.rowSummaryLabel.setText(QCoreApplication.translate("MainWindow", u"Versions in set", None))
        self.addColumnButton.setText(QCoreApplication.translate("MainWindow", u"Add Version Per Passage", None))
        self.removeColumnButton.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.columnSummaryLabel.setText(QCoreApplication.translate("MainWindow", u"Versions per passage", None))
        self.outputLabel.setText(QCoreApplication.translate("MainWindow", u"\n"
"Output Folder", None))
        self.templateLabel.setText(QCoreApplication.translate("MainWindow", u"\n"
"Template", None))
        self.templateIconLabel.setText(QCoreApplication.translate("MainWindow", u"IconLabel", None))
        self.templatePathLabel.setText(QCoreApplication.translate("MainWindow", u"templatePathLabel", None))
        self.templateSelectButton.setText(QCoreApplication.translate("MainWindow", u"Select...", None))
        self.templateShowButton.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.outputDirIconLabel.setText(QCoreApplication.translate("MainWindow", u"conLabel", None))
        self.outputDirPathLabel.setText(QCoreApplication.translate("MainWindow", u"outputDirPathLabel", None))
        self.outputDirSelectButton.setText(QCoreApplication.translate("MainWindow", u"Select...", None))
        self.outputDirShowButton.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.planConfigButton.setText(QCoreApplication.translate("MainWindow", u"Plan Options...", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start...", None))
        self.toggleSourceButton.setText(QCoreApplication.translate("MainWindow", u"Toggle Source", None))
        self.planNotesTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Plan Notes", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

