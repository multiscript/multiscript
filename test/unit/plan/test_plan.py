import unittest
from pathlib import Path, PureWindowsPath, PurePosixPath
import platform

import multiscript.plan


class TestPlan(unittest.TestCase):

    def abs_path(self, str_or_path):
        if platform.system() == "Windows":
            return Path("C:", str_or_path)
        else:
            return Path(str_or_path)

    def test_plan_paths(self):
        plan = multiscript.plan.Plan()

        # Test absolute paths correctly become relative
        plan.path = self.abs_path("/Path/To/Plan/plan.mplan")
        plan.template_path = self.abs_path("/Path/To/Plan/Templates/template.txt")
        plan.output_dir_path = self.abs_path("/Path/To/Plan/Output/")
        self.assertEqual(plan.template_path, Path("Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("Output"))

        # Test absolute paths correctly stay absolute
        plan.template_path = self.abs_path("/Path/To/Somewhere/Else/Templates/template.txt")
        plan.output_dir_path = self.abs_path("/Path/To/Somewhere/Else/Output/")
        self.assertEqual(plan.template_path, self.abs_path("/Path/To/Somewhere/Else/Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, self.abs_path("/Path/To/Somewhere/Else/Output/"))

        # Test relative paths stay relative
        plan.template_path = Path("Templates/template.txt")
        plan.output_dir_path = Path("Output")
        self.assertEqual(plan.template_path, Path("Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("Output"))

        # Test absolute paths calculated correctly
        plan.path = self.abs_path("/Path/To/Plan/plan.mplan")
        plan.template_path = Path("Templates/template.txt")
        plan.output_dir_path = Path("Output")
        self.assertEqual(plan.template_abspath, self.abs_path("/Path/To/Plan/Templates/template.txt"))
        self.assertEqual(plan.output_dir_abspath, self.abs_path("/Path/To/Plan/Output"))
        plan.path = self.abs_path("/Path/To/Somewhere/Else/plan.mplan")
        self.assertEqual(plan.template_abspath, self.abs_path("/Path/To/Somewhere/Else/Templates/template.txt"))
        self.assertEqual(plan.output_dir_abspath, self.abs_path("/Path/To/Somewhere/Else/Output"))

        # Test moving the plan recalcuates paths correctly
        plan.path = self.abs_path("/Path/To/Plan/plan.mplan")
        plan.template_path = self.abs_path("/Path/To/Somewhere/Else/Templates/template.txt")
        plan.output_dir_path = self.abs_path("/Path/To/Somewhere/Else/Output/")
        self.assertEqual(plan.template_path, self.abs_path("/Path/To/Somewhere/Else/Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, self.abs_path("/Path/To/Somewhere/Else/Output/"))
        plan.path = self.abs_path("/Path/To/Different/Location/plan.mplan")
        self.assertEqual(plan.template_path, self.abs_path("/Path/To/Somewhere/Else/Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, self.abs_path("/Path/To/Somewhere/Else/Output/"))
        plan.path = self.abs_path("/Path/To/Somewhere/Else/plan.mplan")
        self.assertEqual(plan.template_path, Path("Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("Output"))

    @unittest.skip("Demo of pathlib flavour conversion requirements")
    def test_path_conversion_demo(self):
        path_strings = ["C:\\abs\\win\\path\\backslashes",
                        "C:/abs/win/path/fwdslashes",
                        "/abs/posix/path",
                        "relative\\path\\backslashes",
                        "relative/path/fwdslashes"
                       ]
        
        print("\nDemo strings:")
        for s in path_strings:
            print(s)

        print("\nPurePosixPath(s) doesn't detects the path parts when there's backslashes")
        for s in path_strings:
            print("repr(PurePosixPath(s)):                             ", repr(PurePosixPath(s)))
            print("PurePosixPath(s):                                   ", PurePosixPath(s))
            print("PurePosixPath(s).parts:                             ", PurePosixPath(s).parts)
            print()

        print("\nPureWindowsPath(s) works okay")
        for s in path_strings:
            print("repr(PureWindowsPath(s)):                           ", repr(PureWindowsPath(s)))
            print("PureWindowsPath(s):                                 ", PureWindowsPath(s))
            print("PureWindowsPath(s).parts:                           ", PureWindowsPath(s).parts)
            print()

        print("\nPureWindowsPath(s).as_posix() converts everything to forward slashes")
        for s in path_strings:
            print("PureWindowsPath(s).as_posix()                       ", PureWindowsPath(s).as_posix())

        print("\nPurePosixPath(PureWindowsPath(s).as_posix()) works okay")
        for s in path_strings:
            print("PurePosixPath(PureWindowsPath(s).as_posix())        ", PurePosixPath(PureWindowsPath(s).as_posix()))
            print("PurePosixPath(PureWindowsPath(s).as_posix()).parts  ", PurePosixPath(PureWindowsPath(s).as_posix()).parts)
            print()

        print("\nPureWindowsPath(PureWindowsPath(s).as_posix()) works okay")
        for s in path_strings:
            print("PureWindowsPath(PureWindowsPath(s).as_posix())      ", PureWindowsPath(PureWindowsPath(s).as_posix()))
            print("PureWindowsPath(PureWindowsPath(s).as_posix()).parts", PureWindowsPath(PureWindowsPath(s).as_posix()).parts)
            print()

        print("\nLet p = PurePosixPath(PureWindowsPath(s).as_posix())")
        print("Converting straight to PureWindowsPath doesn't preserve absolute paths. You have to go via as_posix()")
        for s in path_strings:
            p = PurePosixPath(PureWindowsPath(s).as_posix())
            print("p                                                   ", p)
            print("PureWindowsPath(p):                                 ", PureWindowsPath(p))
            print("PureWindowsPath(p).parts:                           ", PureWindowsPath(p).parts)
            print("PureWindowsPath(p).is_absolute():                   ", PureWindowsPath(p).is_absolute())
            print("PureWindowsPath(p.as_posix()):                      ", PureWindowsPath(p.as_posix()))
            print("PureWindowsPath(p.as_posix()).parts:                ", PureWindowsPath(p.as_posix()).parts)
            print("PureWindowsPath(p.as_posix()).is_absolute():        ", PureWindowsPath(p.as_posix()).is_absolute())
            print()

        print("\nLet p = PureWindowsPath(PureWindowsPath(s).as_posix())")
        print("Converting straight to PurePosixPath doesn't preserve absolute paths. You have to go via as_posix()")
        for s in path_strings:
            p = PureWindowsPath(PureWindowsPath(s).as_posix())
            print("p                                                 ", p)
            print("PurePosixPath(p):                                 ", PurePosixPath(p))
            print("PurePosixPath(p).parts:                           ", PurePosixPath(p).parts)
            print("PurePosixPath(p).is_absolute():                   ", PurePosixPath(p).is_absolute())
            print("PurePosixPath(p.as_posix()):                      ", PurePosixPath(p.as_posix()))
            print("PurePosixPath(p.as_posix()).parts:                ", PurePosixPath(p.as_posix()).parts)
            print("PurePosixPath(p.as_posix()).is_absolute():        ", PurePosixPath(p.as_posix()).is_absolute())
            print()

        print
        print("Therefore, when receiving a path string s that could have been created as the opposite flavour")
        print("to the current platform (Windows vs POSIX), it's most reliable to construct a Path using:")
        print("     p = Path(PureWindowsPath(s).as_posix())")
        print("Then, if you wish to perform a test using a particular flavour, always convert via as_posix().")
        print("For example:")
        print("     PureWindowsPath(p.as_posix()).is_absolute()")
        print("     PurePosixPath(p.as_posix()).is_absolute()")
