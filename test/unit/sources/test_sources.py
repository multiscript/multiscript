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

    def test_module_metadata(self):
        source = TEST_APP.source('multiscript-builtin/accordancebible.com')
        metadata = source.module_metadata
        # from pprint import pprint
        # pprint(metadata)

    def test_module_name_db(self):
        source = TEST_APP.source('multiscript-builtin/accordancebible.com')
        db = source.module_name_db
        # print(db)

    def test_module_ui_names(self):
        source = TEST_APP.source('multiscript-builtin/accordancebible.com')
        names = source.module_ui_names
        # print(names)

    def test_all_modules_have_correct_ui_name(self):
        source = TEST_APP.source('multiscript-builtin/accordancebible.com')
        ui_names = set(source.module_ui_names)

        for module_id in source.module_metadata.keys():
            ui_name = source.get_module_ui_name(module_id)
            # print(f"{module_id}: {ui_name}")
            ui_names.remove(ui_name) # Will fail if ui_name not in ui_names

    @unittest.skip
    def test_explore_module_naming(self, show_all=True,
                                   show_human_name_not_in_ui=False,
                                   show_unequal_names=False,
                                   show_no_ui_name=False):
        source = TEST_APP.source('multiscript-builtin/accordancebible.com')
        all_metadata = source.module_metadata
        db = source.module_name_db
        ui_names = source.module_ui_names
        ui_names_remaining = set(ui_names)

        print()
        for id, metadata in all_metadata.items():
            human_name = metadata.get('com.oaktree.module.humanreadablename', None)
            db_name = db.get(id, None)
            names_equal = human_name is not None and db_name is not None and human_name == db_name
            names_unequal = human_name is not None and db_name is not None and human_name != db_name
            
            human_name_in_ui = (human_name in ui_names)
            db_name_in_ui = (db_name in ui_names)
            id_in_ui = (id in ui_names)
            if show_all or \
                (show_human_name_not_in_ui and human_name is not None and not human_name_in_ui) or \
                (show_unequal_names and names_unequal) or \
                (show_no_ui_name and not human_name_in_ui and not db_name_in_ui and not id_in_ui):
                print(f"Human name: {human_name}")
                print(f"DB name{' (same)' if names_equal else ''}: {db_name}")
                print(f"ID: {id}")
                print(f"In UI: {human_name_in_ui}, {db_name_in_ui}, {id_in_ui}")
                print()

            ui_names_remaining -= set([id, human_name, db_name])

            self.assertTrue(human_name_in_ui or db_name_in_ui or id_in_ui)            
        
        print()
        print(f"UI names without module found: {ui_names_remaining}")
