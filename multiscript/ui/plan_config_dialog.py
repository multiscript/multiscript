
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt

import multiscript
from multiscript.ui.plan_config_dialog_generated import Ui_PlanConfigDialog


class PlanConfigDialog(QtWidgets.QDialog, Ui_PlanConfigDialog):
    def __init__(self, parent, plan):
        super().__init__(parent)
        self.plan = plan
        self.source_plan_config_widgets = {}
        self.output_plan_config_widgets = {}
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self.accepted.connect(self.on_accepted)

        self.general_plan_config_widget = self.plan.config.general.new_config_widget()
        if self.general_plan_config_widget is not None:
            self.topTabWidget.insertTab(0, self.general_plan_config_widget, "General")
            self.topTabWidget.setCurrentIndex(0)
            self.general_plan_config_widget.load_config(self.plan.config.general)

        self.source_plan_config_widgets = {}
        for long_id, source_plan_config in self.plan.config.sources.items():
            source_plan_config_widget = source_plan_config.new_config_widget()
            if source_plan_config_widget is not None:
                self.source_plan_config_widgets[long_id] = source_plan_config_widget
                self.sourcesTabWidget.addTab(source_plan_config_widget, multiscript.app().source(long_id).name)
                source_plan_config_widget.load_config(source_plan_config)
        self.topTabWidget.setTabEnabled(self.topTabWidget.indexOf(self.sourcesPage),
                                        len(self.source_plan_config_widgets) > 0)

        self.output_plan_config_widgets = {}
        for long_id, output_plan_config in self.plan.config.outputs.items():
            output_plan_config_widget = output_plan_config.new_config_widget()
            if output_plan_config_widget is not None:
                self.output_plan_config_widgets[long_id] = output_plan_config_widget
                self.outputsTabWidget.addTab(output_plan_config_widget, multiscript.app().output(long_id).name)
                output_plan_config_widget.load_config(output_plan_config)
        self.topTabWidget.setTabEnabled(self.topTabWidget.indexOf(self.outputsPage),
                                        len(self.output_plan_config_widgets) > 0)


    def on_accepted(self):
        if self.general_plan_config_widget is not None:
            self.general_plan_config_widget.save_config(self.plan.config.general)
        
        for long_id, source_plan_config_widget in self.source_plan_config_widgets.items():
            source_plan_config_widget.save_config(self.plan.config.sources[long_id])        
        
        for long_id, output_plan_config_widget in self.output_plan_config_widgets.items():
            output_plan_config_widget.save_config(self.plan.config.outputs[long_id])