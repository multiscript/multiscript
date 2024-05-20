import unittest

from multiscript.plan.combinations import get_all_version_combos, BibleVersionColumn, BibleVersionCombo, BibleVersionComboElement
from multiscript.sources.base import BibleVersion

class TestBibleVersionCombos(unittest.TestCase):
    def test_version_combos(self):
        version_A1 = BibleVersion(abbrev="A1")
        version_B1 = BibleVersion(abbrev="B1")
        version_B2 = BibleVersion(abbrev="B2")
        version_C1 = BibleVersion(abbrev="C1")
        version_C2 = BibleVersion(abbrev="C2")
        version_C3 = BibleVersion(abbrev="C3")

        column_A = BibleVersionColumn([version_A1], 0)
        column_B = BibleVersionColumn([version_B1, version_B2], 1)
        column_C = BibleVersionColumn([version_C1, version_C2, version_C3], 2)

        combo_element_A_A1 = BibleVersionComboElement(column_A, version_A1)
        combo_element_B_B1 = BibleVersionComboElement(column_B, version_B1)
        combo_element_B_B2 = BibleVersionComboElement(column_B, version_B2)
        combo_element_C_C1 = BibleVersionComboElement(column_C, version_C1)
        combo_element_C_C2 = BibleVersionComboElement(column_C, version_C2)
        combo_element_C_C3 = BibleVersionComboElement(column_C, version_C3)

        expected_combos = [BibleVersionCombo([combo_element_A_A1, combo_element_B_B1, combo_element_C_C1]),
                           BibleVersionCombo([combo_element_A_A1, combo_element_B_B1, combo_element_C_C2]),
                           BibleVersionCombo([combo_element_A_A1, combo_element_B_B1, combo_element_C_C3]),
                           BibleVersionCombo([combo_element_A_A1, combo_element_B_B2, combo_element_C_C1]),
                           BibleVersionCombo([combo_element_A_A1, combo_element_B_B2, combo_element_C_C2]),
                           BibleVersionCombo([combo_element_A_A1, combo_element_B_B2, combo_element_C_C3]),
                          ]

        actual_version_combos = get_all_version_combos([column_A, column_B, column_C])
        self.assertEqual(expected_combos, actual_version_combos)

        version_combo = BibleVersionCombo([combo_element_A_A1, combo_element_B_B1, combo_element_C_C1])
        self.assertFalse(version_combo.is_partial)
        template_combo = BibleVersionCombo([combo_element_A_A1, combo_element_B_B1,
                                            BibleVersionComboElement(column_C, None)])
        self.assertTrue(template_combo.is_partial)
        self.assertEqual(version_combo.template_combo, template_combo)