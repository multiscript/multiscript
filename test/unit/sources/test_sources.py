import unittest
from collections import Counter

from multiscript.plugins import BUILTIN_PLUGIN_ID
from multiscript.sources.getbible_dot_net import GetBibleDotNetSource
from multiscript.sources.accordance import AccordanceSource

from test.application import TEST_APP, MultiscriptAppTestCase


class TestBibleSource(MultiscriptAppTestCase):
    def test_builtin_source_list(self):
        builtin_plugin = TEST_APP.plugin(BUILTIN_PLUGIN_ID)
        source_classes = [type(source) for source in builtin_plugin.all_sources]
        
        expected_classes = set([GetBibleDotNetSource, AccordanceSource])
        self.assertEqual(Counter(source_classes), Counter(expected_classes))

    def test_getbible_dot_net_source(self):
        source = TEST_APP.source('multiscript-builtin/getbible.net')
        source.get_all_versions(None)


class TestAccordanceSource(MultiscriptAppTestCase):
    def test_versions(self):
        source = TEST_APP.source('multiscript-builtin/accordancebible.com')
        source.get_all_versions(None)
    
    def test_module_ui_names(self):
        source = TEST_APP.source('multiscript-builtin/accordancebible.com')
        names = source.module_ui_names
        print(names)

    def test_module_name_db(self):
        source = TEST_APP.source('multiscript-builtin/accordancebible.com')
        db = source.module_name_db
        print(db)

