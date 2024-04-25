
from multiscript.qt_custom.model_columns import AttributeColumn

from multiscript.qt_custom.widgets import OutputConfigSubform
from multiscript.outputs.word.version_config_word_panel_generated import Ui_WordVersionConfigPanel


class WordVersionConfigPanel(OutputConfigSubform, Ui_WordVersionConfigPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi(self)

    def _str_to_font_size_num(self, string):
        num = 0
        try:
            num = float(string)
        except Exception:
            pass
        return 0.5 * round(num/0.5)
    
    def _font_size_num_to_str(self, font_size):
        if font_size < 0.5:
            return ""
        else:
            return str(font_size)

    def add_mappings(self, form, bible_output, *args, **kwargs):
        output_long_id = bible_output.long_id
        form.add_model_column_and_widget(
                AttributeColumn("Font Size", lambda version: \
                                self._font_size_num_to_str(version.output_config[output_long_id].font_size),
                                lambda version, value: \
                                setattr(version.output_config[output_long_id], "font_size",
                                        self._str_to_font_size_num(value)),
                                hide=True),
                self.fontSizeLineEdit
        )
