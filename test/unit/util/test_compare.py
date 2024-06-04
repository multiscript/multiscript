import unittest
import os
from pathlib import Path
import secrets
import tempfile
import shutil
import time
import filecmp

from multiscript.util import compare


class TestCompare(unittest.TestCase):
    def test_compare(self):
        bytes_1 = secrets.token_bytes(2048)
        bytes_2 = secrets.token_bytes(2048)
        bytes_3 = secrets.token_bytes(2048)
        bytes_4 = secrets.token_bytes(2048)
       
        with tempfile.TemporaryDirectory() as temp_dir:
            path_1 = Path(temp_dir, "file_1")
            path_2 = Path(temp_dir, "file_2")
            path_3 = Path(temp_dir, "file_3")

            # Duplicate files should compare equal
            self._write_binfile(path_1, bytes_1)
            self._write_binfile(path_2, bytes_1)
            self.assertTrue(compare.cmp_file(path_1, path_2))

            # Different files should compare unequal
            self._write_binfile(path_3, bytes_3)
            self.assertNotEqual(bytes_1, bytes_3)
            self.assertFalse(compare.cmp_file(path_1, path_3))

            # Create a set of directories for comparison
            dirpath_1 = Path(temp_dir, "dir_1")
            dirpath_1.mkdir()
            dirpath_2 = Path(temp_dir, "dir_2")
            dirpath_2.mkdir()
            dirpath_3 = Path(temp_dir, "dir_3")
            dirpath_3.mkdir()

            self._write_binfile(Path(dirpath_1, "file_1"), bytes_1)
            self._write_binfile(Path(dirpath_2, "file_1"), bytes_1)
            self._write_binfile(Path(dirpath_3, "file_1"), bytes_1)

            self._write_binfile(Path(dirpath_1, "file_2"), bytes_2)
            self._write_binfile(Path(dirpath_2, "file_2"), bytes_2)
            self._write_binfile(Path(dirpath_3, "file_2"), bytes_2)

            Path(dirpath_1,"subdir").mkdir()
            Path(dirpath_2,"subdir").mkdir()
            Path(dirpath_3,"subdir").mkdir()

            self._write_binfile(Path(dirpath_1, "subdir", "file_3"), bytes_3)
            self._write_binfile(Path(dirpath_2, "subdir", "file_3"), bytes_3)
            # Dir 3 file 3 has different content
            self.assertNotEqual(bytes_3, bytes_4)
            self._write_binfile(Path(dirpath_3, "subdir", "file_3"), bytes_4)
            self.assertFalse(compare.cmp_file(Path(dirpath_1, "subdir", "file_3"),
                                              Path(dirpath_3, "subdir", "file_3")))
            
            # Directories with duplicate content should compare equal
            self.assertTrue(compare.cmp_dir(dirpath_1, dirpath_2))

            # Directories with one file different should compare unequal
            result = compare.cmp_dir(dirpath_1, dirpath_3)
            self.assertFalse(result)

            # # Zip files of directories with duplicate content should compare equal
            zippath_1 = shutil.make_archive(dirpath_1, "zip", dirpath_1)
            zippath_2 = shutil.make_archive(dirpath_2, "zip", dirpath_2)
            self.assertTrue(compare.cmp_file(zippath_1, zippath_2))

            # # Zip files of directories with different content should compare unequal
            zippath_3 = shutil.make_archive(dirpath_3, "zip", dirpath_3)
            self.assertFalse(compare.cmp_file(zippath_1, zippath_3))

    def _write_binfile(self, path, bytes):
        with open(path, 'wb') as file:
            file.write(bytes)

