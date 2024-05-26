import unittest
from pathlib import Path

import multiscript.plan


class TestPlan(unittest.TestCase):
    def test_paths(self):
        plan = multiscript.plan.Plan()

        # Test absolute paths correctly become relative
        plan.path = Path("/Path/To/Plan/plan.mplan")
        plan.template_path = Path("/Path/To/Plan/Templates/template.txt")
        plan.output_dir_path = Path("/Path/To/Plan/Output/")
        self.assertEqual(plan.template_path, Path("Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("Output"))

        # Test absolute paths correctly stay absolute
        plan.template_path = Path("/Path/To/Somewhere/Else/Templates/template.txt")
        plan.output_dir_path = Path("/Path/To/Somewhere/Else/Output/")
        self.assertEqual(plan.template_path, Path("/Path/To/Somewhere/Else/Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("/Path/To/Somewhere/Else/Output/"))

        # Test relative paths stay relative
        plan.template_path = Path("Templates/template.txt")
        plan.output_dir_path = Path("Output")
        self.assertEqual(plan.template_path, Path("Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("Output"))

        # Test absolute paths calculated correctly
        plan.path = Path("/Path/To/Plan/plan.mplan")
        plan.template_path = Path("Templates/template.txt")
        plan.output_dir_path = Path("Output")
        self.assertEqual(plan.template_abspath, Path("/Path/To/Plan/Templates/template.txt"))
        self.assertEqual(plan.output_dir_abspath, Path("/Path/To/Plan/Output"))
        plan.path = Path("/Path/To/Somewhere/Else/plan.mplan")
        self.assertEqual(plan.template_abspath, Path("/Path/To/Somewhere/Else/Templates/template.txt"))
        self.assertEqual(plan.output_dir_abspath, Path("/Path/To/Somewhere/Else/Output"))

        # Test moving the plan recalcuates paths correctly
        plan.path = Path("/Path/To/Plan/plan.mplan")
        plan.template_path = Path("/Path/To/Somewhere/Else/Templates/template.txt")
        plan.output_dir_path = Path("/Path/To/Somewhere/Else/Output/")
        self.assertEqual(plan.template_path, Path("/Path/To/Somewhere/Else/Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("/Path/To/Somewhere/Else/Output/"))
        plan.path = Path("/Path/To/Different/Location/plan.mplan")
        self.assertEqual(plan.template_path, Path("/Path/To/Somewhere/Else/Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("/Path/To/Somewhere/Else/Output/"))
        plan.path = Path("/Path/To/Somewhere/Else/plan.mplan")
        self.assertEqual(plan.template_path, Path("Templates/template.txt"))
        self.assertEqual(plan.output_dir_path, Path("Output"))



