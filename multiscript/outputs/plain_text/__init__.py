
import logging


from multiscript.outputs.base import OutputVersionConfig, OutputPlanConfig, OutputPlanRun, OutputBibleStreamHandler
from multiscript.outputs.tagged import TaggedOutput, TaggedDocCursor, Tags
from multiscript.outputs.plain_text.plain_text_plan_config_panel import PlainTextPlanConfigPanel
from multiscript.plan.symbols import column_symbols


_logger = logging.getLogger(__name__)

RLM = chr(0x200F) # Unicode RIGHT-TO-LEFT MARK: Single character indicating right-to-left text
RLI = chr(0x2067) # Unicode RIGHT-TO-LEFT ISOLATE: Start of isolated text where base direction is right-to-left
PDI = chr(0x2069) # Unicode POP DIRECTIONAL ISOLATE: Ends isolated text


class PlainTextOutput(TaggedOutput):
    
    ID = "plain_text"

    def __init__(self, plugin):
        super().__init__(plugin)
        self.id = PlainTextOutput.ID
        self.name = "Plain Text"
        self.output_file_ext = ".txt"
        self._accepted_template_exts.append(".txt")

    #
    # Implementation of abstract methods from BibleOutput
    #
    
    def new_output_version_config(self):
        return None

    def new_output_app_config(self):
        return None

    def new_output_plan_config(self):
        return PlainTextPlanConfig(self)

    def new_output_plan_run(self, plan):
        return PlainTextPlanRun(plan)

    def setup(self, runner):
        '''Overriden from TaggedOutput.setup(). Called prior to looping through the version
        combos.

        We use this method to set some defaults for the run.
        '''
        super().setup(runner)
        runner.output_runs[self.long_id].text_join = runner.plan.config.outputs[self.long_id].join_passage_text
    
    #
    # Implementation of abstract methods from FileSetOutput
    #

    def load_document(self, runner, version_combo, template_path):
        with open(template_path, 'r', encoding='utf-8') as file:
            document = PlainTextDocument(file.read())
        return document
    
    def save_document(self, runner, version_combo, document, filepath):
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(str(document))

    #
    # Implementation of abstract methods from TaggedOutput
    #    

    def replace_tag_directly(self, document, tag_text, replacement_text):
        '''Searches document for tag_text, and replaces it with replacement_text.
        Tries to leave surrounding text in the paragraph untouched, though unfortunately
        sometimes the formatting is lost. If tag_text is not found, the document is not modified.
        '''
        document.replace(tag_text, replacement_text)

    def replace_tag_with_cursor(self, document, tag_text):
        '''Searches document for tag_text, removes it and returns a subclass of TaggedDocCursor
        pointing to the paragraph. If not tag_text is not found, returns None.
        '''
        index = document.find(tag_text)
        if index == -1:
            # tag_text not found
            return None

        document.remove_at(index, len(tag_text))
        # The index is still valid even after we remove the tag text
        return PlainTextDocCursor(document, index)

    def new_bible_stream_handler(self, runner, cursor):
        stream_handler = PlainTextBibleStreamHandler(cursor)
        stream_handler.tab_text = runner.plan.config.outputs[self.long_id].tab_text
        stream_handler.after_para_text = runner.plan.config.outputs[self.long_id].after_para_text
        stream_handler.insert_para_tab = runner.plan.config.outputs[self.long_id].insert_para_tab
        stream_handler.skip_initial_para = runner.plan.config.outputs[self.long_id].skip_initial_para
        stream_handler.use_poetry_tabs = runner.plan.config.outputs[self.long_id].use_poetry_tabs
        return stream_handler

    def text_found(self, document, search_text):
        '''Searches document for search_text, and returns True if found, else False.
        '''
        return document.contains(search_text)

    def insert_passage_group_tag(self, runner, document, cursor, is_first, tag_text):
        '''Called when expanding base template tags. Formats the document
        for a passage group header, and then actually inserts the tag_text.

        first_group is True if this is the first passage group header being inserted.
        '''
        cursor.add_text(tag_text + "\n\n")

    def insert_passage_group_table(self, runner, document, cursor, is_first, table_text_array):
        '''Called when expanding base template tags. Inserts a passage group table at the current
        cursor point and then inserts the text in table_text_array into that table, adding any
        formatting necessary.
        '''
        for column_index in range(len(table_text_array[0])):
            for row_index in range(len(table_text_array)):
                cursor.add_text(table_text_array[row_index][column_index] + "\n\n")

    def insert_copyright_table(self, runner, document, cursor, table_text_array):
        '''Called when expanding base template tags. If cursor is not None, inserts a copyright
        table at the current cursor point. If cursor is None, inserts a copyright table at the
        end of the document.
        '''
        if cursor is None:
            cursor = PlainTextDocCursor(document, len(document._text)-1)
        for column_index in range(len(table_text_array[0])):
            for row_index in range(len(table_text_array)):
                cursor.add_text(table_text_array[row_index][column_index] + "\n\n")

    def format_bible_text_tag(self, runner, document, contents_index, column_symbol, bible_content, cursor):
        '''Performs any formatting needed prior to Bible content being inserted.
        '''
        cursor.para_is_rtl = bible_content.bible_version.is_rtl

    def format_copyright_text_tag(self, runner, document, bible_content, cursor):
        '''Performs any formatting needed prior to copyright text being inserted.
        '''
        pass


class PlainTextDocument:
    '''A wrapper to a string containg the entire plain-text document. Because Python strings are
    immutable and multiple objects may wish to update document, we use this wrapper class to
    maintain the master reference to the current document string.
    '''
    def __init__(self, text):
        self._text = text
    
    def contains(self, text):
        return (text in self._text)

    def find(self, text):
        return self._text.find(text)

    def append(self, text):
        self._text = self._text + text

    def replace(self, old_text, new_text):
        self._text = self._text.replace(old_text, new_text)

    def insert_at(self, text, index):
        self._text = self._text[:index] + text + self._text[index:]

    def remove_at(self, index, remove_len):
        self._text = self._text[:index] + self._text[(index+remove_len):]

    def __str__(self):
        return self._text


class PlainTextDocCursor(TaggedDocCursor):
    def __init__(self, document, current_index):
        super().__init__(document)
        self.current_index = current_index
        self.para_is_rtl = False

    def add_new_para(self, text=None):
        self.add_text("\n")
        self.add_text(text)

    def add_new_run(self, text=None):
        self.add_text(text)

    def add_text(self, text):
        if text is not None:
            self.document.insert_at(text, self.current_index)
            self.current_index += len(text)
    

class PlainTextBibleStreamHandler(OutputBibleStreamHandler):
    def __init__(self, cursor):
        self.cursor = cursor

        # Formatting parameters
        self.tab_text = "\t"            # Text to insert when a tab is needed.
        self.after_para_text = ""       # Text to insert after paragraphs
        self.insert_para_tab = True     # True if a tab should be inserted at start of each paragraph
        self.skip_initial_para = False  # If True, don't insert tab at start of the initial paragraph. Only
                                        #   honoured if self.insert_para_tab is true. 
        self.use_poetry_tabs = True     # True if poetry should be indented with a tab

        # Internal state flags
        self._text_started = False      # True once any text has been added
        self._capitalize = False        # True if we're capitalizing all text
        self._in_poetry = False         # True if we're in a poetry paragraph

    def add_text(self, text):
        if self._capitalize:
            text = text.upper()
        self.cursor.add_text(text)
        if len(text.strip()) > 0:
            self._text_started = True

    def add_start_paragraph(self, is_poetry=False):
        # We only add a new paragraph if we've already added some text. This avoids an unnecessary blank
        # paragraph at the start.
        if self._text_started:
            self.cursor.add_new_para()
        if self.cursor.para_is_rtl:
            self.cursor.add_text(RLI) # Needed to ensure punctuation displays well in right-to-left text.
        if is_poetry:                
            self._in_poetry = True
            if self.use_poetry_tabs:
                self.cursor.add_text(self.tab_text)
        else:
            if self._in_poetry:
                # Up to this point we've been in poetry, so don't add a tab.
                pass
            else:
                # Up to this point we have't been in poetry, so do't add a tab.
                if self.insert_para_tab:
                    if self._text_started or not self.skip_initial_para:
                        self.cursor.add_text(self.tab_text)
            # But either way, we're not in poetry now
            self._in_poetry = False

    def add_end_paragraph(self):
        if self.cursor.para_is_rtl:
            self.cursor.add_text(PDI) # End right-to-left text paragraph
        self.cursor.add_text(self.after_para_text)

    def add_line_break(self):
        if self.cursor.para_is_rtl:
            self.cursor.add_text(PDI) # End right-to-left text paragraph
        self.cursor.add_new_para()
        if self.cursor.para_is_rtl:
            self.cursor.add_text(RLI) # Needed to ensure punctuation displays well in right-to-left text.
        if self._in_poetry and self.use_poetry_tabs:
            self.cursor.add_text(self.tab_text)

    def add_start_chap_num(self):
        pass

    def add_end_chap_num(self):
        pass

    def add_start_verse_num(self):
        pass

    def add_end_verse_num(self):
        pass

    def add_start_small_caps(self):
        self._capitalize = True

    def add_end_small_caps(self):
        self._capitalize = False


class PlainTextPlanConfig(OutputPlanConfig):
    def __init__(self, bible_output):
        super().__init__(bible_output)
        self.join_passage_text = "\n[...]\n"    # Text to join grouped texts.
        self.tab_text = "\t"                    # Text to insert when a tab is needed.
        self.after_para_text = ""               # Text to insert after paragraphs
        self.insert_para_tab = True             # True if a tab should be inserted at start of each paragraph
        self.skip_initial_para = False          # If True, don't insert tab at start of the initial paragraph. Only
                                                #   honoured if self.insert_para_tab is true. 
        self.use_poetry_tabs = True             # True if poetry should be indented with a tab

    def new_config_widget(self):
        return PlainTextPlanConfigPanel(None)


class PlainTextPlanRun(OutputPlanRun):
    def __init__(self, plan):
        super().__init__(plan)
