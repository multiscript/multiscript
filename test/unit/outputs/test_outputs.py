import unittest
from collections import Counter

from multiscript.outputs.word import WordOutput
from multiscript.outputs.plain_text import PlainTextOutput

from test.application import TEST_APP

class TestBibleOutput(unittest.TestCase):
    def test_builtin_output_list(self):
        output_classes = [type(output) for output in TEST_APP.all_outputs]
        
        expected_classes = set([WordOutput, PlainTextOutput])
        self.assertEqual(Counter(output_classes), Counter(expected_classes))
