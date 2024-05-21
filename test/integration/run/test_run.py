import contextlib
from enum import Enum, auto
import filecmp
import os
from pathlib import Path
import shutil
import unittest
import tempfile
import zipfile

from test.application import TEST_APP, MultiscriptAppTestCase
import multiscript.plan
import multiscript.plan.runner

#
# See https://stackoverflow.com/questions/4187564/recursively-compare-two-directories-to-ensure-they-have-the-same-files-and-subdi/24860799#24860799
#
class deep_dircmp(filecmp.dircmp):
    '''Subclass filecmp.dircmp to allow for deep file comparisons.
    We only override methods that need to be altered.'''

    def phase3(self): # Find out differences between common files
        xx = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False) # Changed to use shallow=False
        self.same_files, self.diff_files, self.funny_files = xx

    def phase4(self): # Find out differences between common subdirectories
        # A new dircmp object is created for each common subdirectory,
        # these are stored in a dictionary indexed by filename.
        # The hide and ignore properties are inherited from the parent
        self.subdirs = {}
        for x in self.common_dirs:
            a_x = os.path.join(self.left, x)
            b_x = os.path.join(self.right, x)
            self.subdirs[x]  = deep_dircmp(a_x, b_x, self.ignore, self.hide) # Changed to use recursion with our subclass

def is_same(dir1, dir2):
    """
    Compare two directory trees content.
    Return False if they differ, True is they are the same.
    """
    compared = deep_dircmp(dir1, dir2, hide=[os.curdir, os.pardir, '.DS_Store'])
    # compared.report()
    if (compared.left_only or compared.right_only or compared.diff_files 
        or compared.funny_files):
        return False
    for subdir in compared.common_dirs:
        if not is_same(os.path.join(dir1, subdir), os.path.join(dir2, subdir)):
            return False
    return True


class TestRun(MultiscriptAppTestCase):

    class TestMode(Enum):
        TEST     = auto()    # Run the test as normal
        CREATE   = auto()    # Create the expected output, rather than testing for it
        OBSERVE  = auto()    # Observe output: Use known instead of temp directories, don't unzip word docs, don't test
        OBS_TEST = auto()    # Observe output: Use known instead of temp directories, don't unzip word docs, do test

    def test_word_full_run(self, mode=TestMode.TEST):
        ''' Runs a test plan with MS Word template and tests whether the output matches what is expected.

        mode is one of the TestMode enum values.
        '''
        plan_path = Path(__file__, "../../../data/integration/run/test_word_full_run/word_full_run.mplan").resolve()
        template_path = Path(__file__, "../../../../multiscript/templates/Default Template.docx").resolve()
        expected_output_path = plan_path.parent / Path("word_full_run_expected")
        observe_base_path = Path("~/Desktop/TestWordFullRun/").expanduser()

        error_list = []
        plan = multiscript.plan.load(plan_path, error_list)
        for err in error_list:
            print(str(err))

        plan.template_path = template_path

        if mode is TestRun.TestMode.TEST:
            test_output_context_manager = tempfile.TemporaryDirectory()
            expected_expansion_context_manager = tempfile.TemporaryDirectory()
        elif mode is TestRun.TestMode.CREATE:
            expected_output_path.mkdir(parents=True, exist_ok=True)
            test_output_context_manager = contextlib.nullcontext(expected_output_path)
            expected_expansion_context_manager = contextlib.nullcontext(None)
        elif mode is TestRun.TestMode.OBSERVE or mode is TestRun.TestMode.OBS_TEST:
            test_output_dir = Path(observe_base_path, "Output/")
            test_output_dir.mkdir(parents=True, exist_ok=True)
            test_output_context_manager = contextlib.nullcontext(test_output_dir)

            expected_expansion_dir = Path(observe_base_path, "Expected/")
            expected_expansion_dir.mkdir(parents=True, exist_ok=True)
            expected_expansion_context_manager = contextlib.nullcontext(expected_expansion_dir)
        else:
            self.fail("Unknown test mode")

        with test_output_context_manager as test_output_dir:
            # Dir for plan output to be tested against what's expected
            with expected_expansion_context_manager as expected_expansion_dir:
                # Dir for expansion of expected output

                test_output_path = Path(test_output_dir)
                plan.output_dir_path = test_output_path

                plan_runner = multiscript.plan.runner.PlanRunner(plan)
                plan_runner.run()

                if mode is TestRun.TestMode.CREATE:
                    return

                # Copy expected output into expansion directory
                for file in expected_output_path.iterdir():
                    shutil.copy(file, expected_expansion_dir)

                if mode is TestRun.TestMode.OBSERVE:
                    return

                # Expand expected output
                for output_file_path in Path(expected_expansion_dir).glob("*.docx"):
                    extract_dir = output_file_path.with_suffix(output_file_path.suffix + " dir")
                    extract_dir.mkdir()

                    with zipfile.ZipFile(output_file_path) as output_file_zip:
                        output_file_zip.extractall(extract_dir)
                    output_file_path.unlink() # Removes the original docx file

                # Expand the actual output of the plan
                for output_file_path in test_output_path.glob("*.docx"):
                    extract_dir = output_file_path.with_suffix(output_file_path.suffix + " dir")
                    extract_dir.mkdir()

                    with zipfile.ZipFile(output_file_path) as output_file_zip:
                        output_file_zip.extractall(extract_dir)
                    output_file_path.unlink() # Removes the file
                    
                self.assertTrue(is_same(test_output_path, Path(expected_expansion_dir)))

    def test_text_full_run(self, mode=TestMode.TEST):
        ''' Runs a test plan with plain text template and tests whether the output matches what is expected.

        mode is one of the TestMode enum values.
        '''
        plan_path = Path(__file__, "../../../data/integration/run/test_text_full_run/text_full_run.mplan").resolve()
        template_path = Path(__file__, "../../../../multiscript/templates/Default Template.txt").resolve()
        expected_output_path = plan_path.parent / Path("text_full_run_expected")
        observe_base_path = Path("~/Desktop/TestTextFullRun/").expanduser()

        error_list = []
        plan = multiscript.plan.load(plan_path, error_list)
        for err in error_list:
            print(str(err))

        plan.template_path = template_path

        if mode is TestRun.TestMode.TEST:
            test_output_context_manager = tempfile.TemporaryDirectory()
            expected_context_manager = tempfile.TemporaryDirectory()
        elif mode is TestRun.TestMode.CREATE:
            expected_output_path.mkdir(parents=True, exist_ok=True)
            test_output_context_manager = contextlib.nullcontext(expected_output_path)
            expected_context_manager = contextlib.nullcontext(None)
        elif mode is TestRun.TestMode.OBSERVE or mode is TestRun.TestMode.OBS_TEST:
            test_output_dir = Path(observe_base_path, "Output/")
            test_output_dir.mkdir(parents=True, exist_ok=True)
            test_output_context_manager = contextlib.nullcontext(test_output_dir)

            expected_dir = Path(observe_base_path, "Expected/")
            expected_dir.mkdir(parents=True, exist_ok=True)
            expected_context_manager = contextlib.nullcontext(expected_dir)
        else:
            self.fail("Unknown test mode")

        with test_output_context_manager as test_output_dir:
            # Dir for plan output to be tested against what's expected
            with expected_context_manager as expected_dir:
                # Dir for expansion of expected output

                test_output_path = Path(test_output_dir)
                plan.output_dir_path = test_output_path

                plan_runner = multiscript.plan.runner.PlanRunner(plan)
                plan_runner.run()

                if mode is TestRun.TestMode.CREATE:
                    return

                # Copy expected output into expectation directory, using a text copy to handle
                # any difference in platform line-endings.
                for source_path in expected_output_path.glob("*.txt"):
                    with open(source_path, 'r', encoding='utf-8') as source_file:
                        with open(Path(expected_dir, source_path.name), 'w', encoding='utf-8') as dest_file:
                            text = source_file.read()
                            dest_file.write(text)

                if mode is TestRun.TestMode.OBSERVE:
                    return
                    
                self.assertTrue(is_same(test_output_path, Path(expected_dir)))