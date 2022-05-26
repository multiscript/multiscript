import unittest

from multiscript.bible.content import *

class TestBibleContent(unittest.TestCase):
    def test_add_example_tokens(self):
        content = BibleContent()
        content.body.add_start_small_caps()
        content.body.add_text("Hello World")
        content.body.add_end_small_caps()
        
        token_str = str(content.body.tokens.pop(0))
        self.assertEqual(token_str, str(BibleStartSmallCapsToken(None, None)))
        token_str = str(content.body.tokens.pop(0))
        self.assertEqual(token_str, str(BibleTextToken(None, None,"Hello World")))
        token_str = str(content.body.tokens.pop(0))
        self.assertEqual(token_str, str(BibleEndSmallCapsToken(None, None)))
