import unittest
import sys

from multiscript.util.exception_catcher import *
from test.application import TEST_APP


class TestExceptionCatcher(unittest.TestCase):
    def test_exception_catcher_context_manager(self):
        existing_hook = sys.excepthook
        with catch_unhandled_exceptions() as catcher:
            self.assertEqual(sys.excepthook, catcher._excepthook)
        self.assertEqual(sys.excepthook, existing_hook)

    def test_exception_catcher_class(self):
        exception_catcher = UnhandledExceptionCatcher()
        existing_hook = sys.excepthook

        exception_catcher.install_hook()
        self.assertEqual(sys.excepthook, exception_catcher._excepthook)

        exception_catcher.remove_hook()
        self.assertEqual(sys.excepthook, existing_hook)

        
