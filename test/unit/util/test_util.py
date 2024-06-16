
from pathlib import Path, PurePosixPath, PureWindowsPath

import unittest

from multiscript.util import util


class TestCompare(unittest.TestCase):
    def test_is_absolute_any_platform(self):
        self.assertTrue(util.is_absolute_any_platform("C:\\abs\\win\\path\\backslashes"))
        self.assertTrue(util.is_absolute_any_platform("C:/abs/win/path/fwdslashes"))
        self.assertTrue(util.is_absolute_any_platform("/abs/posix/path"))
        self.assertFalse(util.is_absolute_any_platform("relative\\path\\backslashes"))
        self.assertFalse(util.is_absolute_any_platform("relative/path/fwdslashes"))

        self.assertTrue(util.is_absolute_any_platform(PurePosixPath("C:\\abs\\win\\path\\backslashes")))
        self.assertTrue(util.is_absolute_any_platform(PurePosixPath("C:/abs/win/path/fwdslashes")))
        self.assertTrue(util.is_absolute_any_platform(PurePosixPath("/abs/posix/path")))
        self.assertFalse(util.is_absolute_any_platform(PurePosixPath("relative\\path\\backslashes")))
        self.assertFalse(util.is_absolute_any_platform(PurePosixPath("relative/path/fwdslashes")))

        self.assertTrue(util.is_absolute_any_platform(PureWindowsPath("C:\\abs\\win\\path\\backslashes")))
        self.assertTrue(util.is_absolute_any_platform(PureWindowsPath("C:/abs/win/path/fwdslashes")))
        self.assertTrue(util.is_absolute_any_platform(PureWindowsPath("/abs/posix/path")))
        self.assertFalse(util.is_absolute_any_platform(PureWindowsPath("relative\\path\\backslashes")))
        self.assertFalse(util.is_absolute_any_platform(PureWindowsPath("relative/path/fwdslashes")))

        # Final test on whatever platform the test is run on
        self.assertTrue(util.is_absolute_any_platform(Path("C:\\abs\\win\\path\\backslashes")))
        self.assertTrue(util.is_absolute_any_platform(Path("C:/abs/win/path/fwdslashes")))
        self.assertTrue(util.is_absolute_any_platform(Path("/abs/posix/path")))
        self.assertFalse(util.is_absolute_any_platform(Path("relative\\path\\backslashes")))
        self.assertFalse(util.is_absolute_any_platform(Path("relative/path/fwdslashes")))
