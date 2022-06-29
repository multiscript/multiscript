
import ast

from PySide6.QtCore import Qt

from multiscript.qt_custom.widgets import ConfigWidget
from multiscript.outputs.plain_text.plain_text_plan_config_panel_generated import Ui_PlainTextPlanConfigPanel


class PlainTextPlanConfigPanel(ConfigWidget, Ui_PlainTextPlanConfigPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
        self.insertParaTabCheckBox.stateChanged.connect(self.on_insert_para_tab_chceckbox_state_changed)
    
    def load_config(self, config):
        '''Load the contents of config into this widget.
        '''
        self.joinPassageLineEdit.setText(repr(config.join_passage_text)[1:-1]) # Strip leading and trailing quotes
        self.tabTextLineEdit.setText(repr(config.tab_text)[1:-1]) # Strip leading and trailing quotes
        self.afterParaLineEdit.setText(repr(config.after_para_text)[1:-1]) # Strip leading and trailing quotes
        self.insertParaTabCheckBox.setChecked(config.insert_para_tab)
        self.skipInitialParaCheckBox.setChecked(config.skip_initial_para)
        self.usePoetryTabsCheckBox.setChecked(config.use_poetry_tabs)

    def save_config(self, config):
        '''Save the contents of this widget into config.
        '''
        # Adding leading and trailing quotes preserves strings
        config.join_passage_text = ast.literal_eval("'" + self.joinPassageLineEdit.text() + "'")
        config.tab_text = ast.literal_eval("'" + self.tabTextLineEdit.text() + "'")
        config.after_para_text = ast.literal_eval("'" + self.afterParaLineEdit.text() + "'")
        config.insert_para_tab = self.insertParaTabCheckBox.isChecked()
        config.skip_initial_para = self.skipInitialParaCheckBox.isChecked()
        config.use_poetry_tabs = self.usePoetryTabsCheckBox.isChecked()

    def on_insert_para_tab_chceckbox_state_changed(self, state):
        self.skipInitialParaCheckBox.setEnabled(state == Qt.Checked)