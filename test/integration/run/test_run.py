import contextlib
from enum import Enum, auto
import filecmp
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

import multiscript.outputs
import multiscript.outputs.fileset
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
                # Remove plan run record to simplify directory comparison
                Path(test_output_dir, multiscript.plan.runner.PLAN_RUN_RECORD_FILENAME).unlink()

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
                # Remove plan run record to simplify directory comparison
                Path(test_output_dir, multiscript.plan.runner.PLAN_RUN_RECORD_FILENAME).unlink()

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

    def test_fileset_metadata(self):
        '''Tests whether the fileset metadata correct affects which output files are updated.
        '''
        plan_path = Path(__file__,
                         "../../../data/integration/run/test_fileset_metadata/test_fileset_metadata.mplan").resolve()
        template_path = Path(__file__, "../../../../multiscript/templates/Default Template.txt").resolve()

        error_list = []
        plan = multiscript.plan.load(plan_path, error_list)
        for err in error_list:
            print(str(err))

        plan.template_path = template_path

        with tempfile.TemporaryDirectory() as test_output_dir:
            plan.output_dir_path = Path(test_output_dir)

            #
            # Initial run to establish initial metadata
            #
            print("Initial run:")
            plan_runner = multiscript.plan.runner.PlanRunner(plan)
            plan_runner.run()
            base_metadata = plan_runner.run_record.fileset_metadata

            #
            # Re-run (with a fresh PlanRunner) and confirm no file changes
            #
            print("Rerun to confirm no changes:")
            plan_runner = multiscript.plan.runner.PlanRunner(plan)
            plan_runner.run()
            self.assertEqual(base_metadata, plan_runner.run_record.fileset_metadata)

            #
            # Modify one output file and re-run
            #
            print("Modify one output and confirm it's not updated:")
            output_path = Path(test_output_dir, "Gen1.1-4 +3 English-KJV,Chinese (Traditional)-CUT,Spanish-VALERA.txt")
            output_path.touch()
            self._assert_file_changed_and_update_metadata(base_metadata, output_path)
            plan_runner = multiscript.plan.runner.PlanRunner(plan)
            plan_runner.run()
            self.assertEqual(base_metadata, self._metadata_on_disk(test_output_dir))

            #
            # Modify a template file and confirm dependent output files change
            #
            print("Modify a template and confirm dependent files change:")
            output_path = Path(test_output_dir, "Gen1.1-4 +3 English-KJV,Chinese (Traditional)-CUT,-_template.txt")
            # Need to actually change the data in the tempplate in order for dependent files to change
            with open(output_path, "a") as output_file:
                output_file.writelines(["Here's an extra line of text.\n"])
            self._assert_file_changed_and_update_metadata(base_metadata, output_path)
            plan_runner = multiscript.plan.runner.PlanRunner(plan)
            plan_runner.run()

            output_path = Path(test_output_dir, "Gen1.1-4 +3 English-KJV,Chinese (Traditional)-CUT,-.txt")
            self._assert_file_changed_and_update_metadata(base_metadata, output_path)

            output_path = Path(test_output_dir, "Gen1.1-4 +3 English-KJV,Chinese (Traditional)-CUT,Korean-KOREAN.txt")
            self._assert_file_changed_and_update_metadata(base_metadata, output_path)

            output_path = Path(test_output_dir, "Gen1.1-4 +3 English-KJV,Chinese (Traditional)-CUT,French-LS1910.txt")
            self._assert_file_changed_and_update_metadata(base_metadata, output_path)
            # Previous modification to "Gen1.1-4 +3 English-KJV,Chinese (Traditional)-CUT,Spanish-VALERA.txt"
            # prevents it being modified here.
            self.assertEqual(base_metadata, self._metadata_on_disk(test_output_dir))

    def _assert_file_changed_and_update_metadata(self, base_metadata, output_path):
        output_path_metadata = multiscript.outputs.fileset.FileMetaData(output_path)
        self.assertNotEqual(base_metadata[str(output_path)], output_path_metadata)
        base_metadata[str(output_path)] = output_path_metadata

    def _metadata_on_disk(self, test_output_dir):
        on_disk_metadata = {}
        for path in Path(test_output_dir).glob("*.txt"):
            on_disk_metadata[str(path)] = multiscript.outputs.fileset.FileMetaData(path)
        return on_disk_metadata

