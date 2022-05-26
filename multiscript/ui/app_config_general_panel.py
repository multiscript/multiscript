
from multiscript.qt_custom.widgets import ConfigWidget
from multiscript.ui.app_config_general_panel_generated import Ui_GeneralAppConfigPanel


class GeneralAppConfigPanel(ConfigWidget, Ui_GeneralAppConfigPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
    
    def load_config(self, config):
        '''Load the contents of config into this widget.
        '''
        self.savePlansBeforeExecutionCheckBox.setChecked(config.save_plans_before_execution)
        self.keepExistingTemplateFilesCheckBox.setChecked(config.keep_existing_template_files)
        self.keepExistingOutputFilesCheckbox.setChecked(config.keep_existing_output_files)

    def save_config(self, config):
        '''Save the contents of this widget into config.
        '''
        config.save_plans_before_execution = self.savePlansBeforeExecutionCheckBox.isChecked()
        config.keep_existing_template_files = self.keepExistingTemplateFilesCheckBox.isChecked()
        config.keep_existing_output_files = self.keepExistingOutputFilesCheckbox.isChecked()