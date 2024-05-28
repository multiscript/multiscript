
import filecmp
import os
import tempfile
import zipfile


def cmp_file(path_1, path_2):
        if zipfile.is_zipfile(str(path_1)) and zipfile.is_zipfile(str(path_2)):
            # Handle zip files
            with tempfile.TemporaryDirectory() as expand_dir_1, \
                 tempfile.TemporaryDirectory() as expand_dir_2:
                with zipfile.ZipFile(path_1) as zipfile_1, zipfile.ZipFile(path_2) as zipfile_2:
                    zipfile_1.extractall(expand_dir_1)
                    zipfile_2.extractall(expand_dir_2)
                    return cmp_dir(expand_dir_1, expand_dir_2)
        else:
            return filecmp.cmp(str(path_1), str(path_2), shallow=False)

def cmp_dir(path_1, path_2):
    comparison = deep_dircmp(str(path_1), str(path_2), hide=[os.curdir, os.pardir, '.DS_Store'])
    return _comparison_equal(comparison)

def _comparison_equal(comparison):
    if (comparison.left_only or comparison.right_only or comparison.diff_files 
        or comparison.funny_files):
        return False
    for sub_comparison in comparison.subdirs.values():
        if not _comparison_equal(sub_comparison):
            return False
    return True


class deep_dircmp(filecmp.dircmp):
    '''Subclass of filecmp.dircmp to allow for deep file comparisons.'''

    def phase3(self): # Find out differences between common files
        xx = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False) # Changed to use shallow=False
        self.same_files, self.diff_files, self.funny_files = xx

