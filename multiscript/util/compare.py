
from pathlib import Path
import tempfile
import zipfile

#
# On Windows, it proved difficult to test cmp_dir() when implemented using the filecmp library,
# as there seemed to be race conditions around filecmp's internal caching when test files
# had identical sizes and mod-times but different content.
# Therefore, the implementations below do not rely on the filecmp library at all.
#

BUFFER_SIZE = 1024

def cmp_file(path_1: Path, path_2: Path):
        if zipfile.is_zipfile(str(path_1)) and zipfile.is_zipfile(str(path_2)):
            # Handle zip files
            with tempfile.TemporaryDirectory() as expand_dir_1, \
                 tempfile.TemporaryDirectory() as expand_dir_2:
                with zipfile.ZipFile(path_1) as zipfile_1, zipfile.ZipFile(path_2) as zipfile_2:
                    zipfile_1.extractall(expand_dir_1)
                    zipfile_2.extractall(expand_dir_2)
                    return cmp_dir(expand_dir_1, expand_dir_2)
        else:
            if path_1.stat().st_size != path_2.stat().st_size:
                return False
            with open(path_1, 'rb') as file_1, open(path_2, 'rb') as file_2:
                while True:
                    bytes_1 = file_1.read(BUFFER_SIZE)
                    bytes_2 = file_2.read(BUFFER_SIZE)
                    if bytes_1 != bytes_2:
                        return False
                    if not bytes_1:
                        return True

def cmp_dir(path_1, path_2):
    path_1 = Path(path_1)
    path_2 = Path(path_2)
    subpaths_1 = {} # Keys: relative path, Values: absolute path
    subpaths_2 = {} # Keys: relative path, Values: absolute path
    for subpath in path_1.glob("**/*"):
        subpaths_1[subpath.relative_to(path_1)] = subpath
    for subpath in path_2.glob("**/*"):
        subpaths_2[subpath.relative_to(path_2)] = subpath
    # The two sets of relative paths should be identical
    if set(subpaths_1.keys()) != set(subpaths_2.keys()):
        return False
    # Compare individual files
    for relpath in subpaths_1.keys():
        subpath_1 = subpaths_1[relpath]
        subpath_2 = subpaths_2[relpath]
        if not subpath_1.is_dir() and not cmp_file(subpath_1, subpath_2):
            return False
    return True
