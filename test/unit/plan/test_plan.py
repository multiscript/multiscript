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
