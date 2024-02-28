import difflib
from pprint import pformat
from pathlib import Path
import tempfile
import unittest

from multiscript.plan import Plan, load
from multiscript.plugins import BUILTIN_PLUGIN_ID
from test.application import TEST_APP, MultiscriptAppTestCase


def text_diff(path1, path2):
    with open(path1) as file:
        path1_lines = file.readlines()
    with open(path2) as file:
        path2_lines = file.readlines()
    return ''.join(difflib.unified_diff(path1_lines, path2_lines))


class TestPlan(MultiscriptAppTestCase):
    def test_plan_save_and_load(self):
        versions = []
        for source in TEST_APP.plugin(BUILTIN_PLUGIN_ID).all_sources:
            versions += source.get_all_versions()
        
        with tempfile.TemporaryDirectory() as tempdir_name:
            plan_path = Path(tempdir_name) / "temp_plan.mplan"
        
            plan = Plan()

            plan.path = plan_path
            plan.bible_versions = versions
            plan.new = False
            before = pformat(plan)
            plan.save()
            
            error_list = []
            plan = load(plan_path, error_list)
            after = pformat(plan)
            for err in error_list:
                print(str(err))
            # diff = difflib.unified_diff(before, after)
            # print(before)
            # print(after)
            # print(''.join(diff),end='')
            self.assertEqual(before, after)

    def test_plan_objects_not_found(self):
        '''Test that plan objects not found are reported and removed.
        '''
        orig_plan_path = (Path(__file__) / Path("../../../data/integration/plan/test_plan_objects_not_found/test_plan_objects_not_found.mplan")).resolve()
        expected_result_path = (Path(__file__) / \
                               Path("../../../data/integration/plan/test_plan_objects_not_found/test_plan_objects_not_found_expected.mplan")).resolve()

        error_list = []
        plan = load(orig_plan_path, error_list)
        self.assertEqual(len(error_list), 4)

        with tempfile.TemporaryDirectory() as tempdir_name:
            path_of_modified_plan = Path(tempdir_name) / "modified_plan.mplan"
            plan.path = path_of_modified_plan
            plan.save()

            self.assertEqual('', text_diff(expected_result_path, path_of_modified_plan))

       
