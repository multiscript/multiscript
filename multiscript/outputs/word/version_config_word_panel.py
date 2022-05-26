
from multiscript.qt_custom.model_columns import AttributeColumn

from multiscript.qt_custom.widgets import OutputConfigSubform
from multiscript.outputs.word.version_config_word_panel_generated import Ui_WordVersionConfigPanel


class WordVersionConfigPanel(OutputConfigSubform, Ui_WordVersionConfigPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)

    def add_mappings(self, form, bible_output, *args, **kwargs):
        output_long_id = bible_output.long_id
        form.add_model_column_and_widget(
                AttributeColumn("Font Name", lambda version: version.output_config[output_long_id].font_name,
                                lambda version, value: \
                                setattr(version.output_config[output_long_id], "font_name", value), hide=True),
                self.fontNameFontComboBox
        )
        form.add_model_column_and_widget(
                AttributeColumn("Font Size", lambda version: version.output_config[output_long_id].font_size,
                                lambda version, value: \
                                setattr(version.output_config[output_long_id], "font_size", value), hide=True),
                self.fontSizeDoubleSpinBox
        )
