
import ast

from multiscript.qt_custom.widgets import ConfigWidget
from multiscript.outputs.word.plan_config_word_panel_generated import Ui_WordPlanConfigPanel


class WordPlanConfigPanel(ConfigWidget, Ui_WordPlanConfigPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)
    
    def load_config(self, config):
        '''Load the contents of config into this widget.
        '''
        self.joinPassageLineEdit.setText(repr(config.join_passage_text)[1:-1]) # Strip leading and trailing quotes
        self.allTablesInsertBlankParasCheckBox.setChecked(config.all_tables_insert_blank_paras)
        self.applyForrmattingToRunsCheckBox.setChecked(config.apply_formatting_to_runs)

    def save_config(self, config):
        '''Save the contents of this widget into config.
        '''
        config.join_passage_text = ast.literal_eval("'" + self.joinPassageLineEdit.text() + "'")
        config.all_tables_insert_blank_paras = self.allTablesInsertBlankParasCheckBox.isChecked()
        config.apply_formatting_to_runs = self.applyForrmattingToRunsCheckBox.isChecked()
