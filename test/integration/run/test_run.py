import filecmp
import os
from pathlib import Path
import shutil
import unittest
import tempfile
import zipfile

from test.application import TEST_APP
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


class TestRun(unittest.TestCase):

    def test_full_run(self, create_expected_output=False):
        ''' Runs a test plan and tests whether the output matches what is expected.

        Run the test plan once with create_expected_ouput set to True to generate the expected
        output files.
        '''
        plan_path = (Path(__file__) / Path("../../../data/integration/run/test_full_run/full_run.mplan")).resolve()
        template_path = (Path(__file__) / Path("../../../../multiscript/templates/Default Template.docx")).resolve()
        expected_output_path = plan_path.parent / Path("full_run_expected")

        error_list = []
        plan = multiscript.plan.load(plan_path, error_list)
        for err in error_list:
            print(str(err))

        plan.template_path = template_path

        # If you need to examine the test output, you can use lines like these instead of the following with statement
        # test_output_dir = Path("/Users/james/Desktop/Test_Full_Run/Output/").resolve()
        # test_output_dir.mkdir(parents=True, exist_ok=True)
        # if True:
        with tempfile.TemporaryDirectory() as test_output_dir:
            # Dir for plan output to be tested against what's expected

            # If you need to examine the test output, you can use lines like these instead of the following with statement
            # expected_expansion_dir = Path("/Users/james/Desktop/Test_Full_Run/Expected/").resolve()
            # expected_expansion_dir.mkdir(parents=True, exist_ok=True)
            # if True:
            with tempfile.TemporaryDirectory() as expected_expansion_dir:
                # Dir for expansion of expected output

                test_output_path = Path(test_output_dir)
                if create_expected_output:
                    plan.output_dir_path = expected_output_path
                else:
                    plan.output_dir_path = test_output_path

                plan_runner = multiscript.plan.runner.PlanRunner(plan)
                plan_runner.run()

                if create_expected_output:
                    return

                # Copy expected output into expansion directory
                for file in expected_output_path.iterdir():
                    shutil.copy(file, expected_expansion_dir)

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
