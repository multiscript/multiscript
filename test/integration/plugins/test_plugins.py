from pathlib import Path
import unittest

from test.application import TEST_APP, MultiscriptAppTestCase

TEST_PLUGIN_ID = "app_multiscript_test_plugin"
TEST_PLUGIN_PATH = (Path(__file__) / Path("../../../data/integration/plugins/test_plugin_add_and_remove/app_multiscript_test_plugin-0.9.0.mplugin")).resolve()


class TestPlan(MultiscriptAppTestCase):
    def test_plugin_add_and_remove(self):
        test_plugin_instance = TEST_APP.plugin(TEST_PLUGIN_ID)
        self.assertIsNone(test_plugin_instance)

        TEST_APP.add_plugin(TEST_PLUGIN_PATH, show_ui=False)
        test_plugin_instance = TEST_APP.plugin(TEST_PLUGIN_ID)
        self.assertIsNotNone(test_plugin_instance)

        # It's difficult to completely test plugin removal, because it relies on an app
        # restart that doesn't work well with our testing framework. So for now
        # we just check the plugin was removed from disk.
        self.assertTrue(test_plugin_instance.base_path.exists())
        TEST_APP.remove_plugin(TEST_PLUGIN_ID, show_ui=False)
        self.assertFalse(test_plugin_instance.base_path.exists())

