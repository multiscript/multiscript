
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

import multiscript
from multiscript.ui.app_config_dialog_generated import Ui_AppConfigDialog


class AppConfigDialog(QtWidgets.QDialog, Ui_AppConfigDialog):
    def __init__(self, parent, app_config_group):
        super().__init__(parent)
        self.app_config_group = app_config_group
        self.source_app_config_widgets = {}
        self.output_app_config_widgets = {}
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        windowTitle = QtWidgets.QApplication.instance().applicationName() + " "
        if multiscript.on_mac():
            windowTitle += "Preferences"
        else:
            windowTitle += "Settings"
        self.setWindowTitle(windowTitle)
        self.accepted.connect(self.on_accepted)

        self.general_app_config_widget = self.app_config_group.general.new_config_widget()
        if self.general_app_config_widget is not None:
            self.topTabWidget.insertTab(0, self.general_app_config_widget, "General")
            self.topTabWidget.setCurrentIndex(0)
            self.general_app_config_widget.load_config(self.app_config_group.general)

        self.source_app_config_widgets = {}
        for long_id, source_app_config in self.app_config_group.sources.items():
            source_app_config_widget = source_app_config.new_config_widget()
            if source_app_config_widget is not None:
                self.source_app_config_widgets[long_id] = source_app_config_widget
                self.sourcesTabWidget.addTab(source_app_config_widget, multiscript.app().source(long_id).name)
                source_app_config_widget.load_config(source_app_config)
        self.topTabWidget.setTabEnabled(self.topTabWidget.indexOf(self.sourcesPage),
                                        len(self.source_app_config_widgets) > 0)

        self.output_app_config_widgets = {}
        for long_id, output_app_config in self.app_config_group.outputs.items():
            output_app_config_widget = output_app_config.new_config_widget()
            if output_app_config_widget is not None:
                self.output_app_config_widgets[long_id] = output_app_config_widget
                self.outputsTabWidget.addTab(output_app_config_widget, multiscript.app().output(long_id).name)
                output_app_config_widget.load_config(output_app_config)
        self.topTabWidget.setTabEnabled(self.topTabWidget.indexOf(self.outputsPage),
                                        len(self.output_app_config_widgets) > 0)

        self.plugins_app_config_widget = self.app_config_group.plugins.new_config_widget()
        if self.plugins_app_config_widget is not None:
            self.topTabWidget.addTab(self.plugins_app_config_widget, "Plugins")
            self.plugins_app_config_widget.load_config(self.app_config_group.plugins)


    def on_accepted(self):
        if self.general_app_config_widget is not None:
            self.general_app_config_widget.save_config(self.app_config_group.general)
        
        for long_id, source_plan_config_widget in self.source_app_config_widgets.items():
            source_plan_config_widget.save_config(self.app_config_group.sources[long_id])        
        
        for long_id, output_plan_config_widget in self.output_app_config_widgets.items():
            output_plan_config_widget.save_config(self.app_config_group.outputs[long_id])

        if self.plugins_app_config_widget is not None:
            self.plugins_app_config_widget.save_config(self.app_config_group.plugins)
 