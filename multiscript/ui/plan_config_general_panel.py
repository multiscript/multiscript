
from PySide2.QtCore import Qt

from multiscript.qt_custom.widgets import ConfigWidget
from multiscript.ui.plan_config_general_panel_generated import Ui_GeneralPlanConfigPanel


class GeneralPlanConfigPanel(ConfigWidget, Ui_GeneralPlanConfigPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self.allowConfirmationsCheckBox.stateChanged.connect(self.allowConfirmationsCheckbox_stateChanged)
        self.allowConfirmationsCheckbox_stateChanged(self.allowConfirmationsCheckBox.checkState())
    
    def load_config(self, config):
        '''Load the contents of config into this widget.
        '''
        self.allowConfirmationsCheckBox.setChecked(config.allow_confirmations)
        self.confirmAfterTemplateExpansionCheckBox.setChecked(config.confirm_after_template_expansion)

    def save_config(self, config):
        '''Save the contents of this widget into config.
        '''
        config.allow_confirmations = self.allowConfirmationsCheckBox.isChecked()
        config.confirm_after_template_expansion = self.confirmAfterTemplateExpansionCheckBox.isChecked()
    
    def allowConfirmationsCheckbox_stateChanged(self, state):
        self.confirmAfterTemplateExpansionCheckBox.setEnabled(state == Qt.CheckState.Checked)