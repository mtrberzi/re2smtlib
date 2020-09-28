import unittest
from re2smtlib import translate_regex_to_smtlib

class TestBasic(unittest.TestCase):
    def test_single_literal(self):
        self.assertEqual(translate_regex_to_smtlib("X"), '(str.to_re "X")')

    def test_escape_character(self):
        self.assertEqual(translate_regex_to_smtlib("\n"), '(str.to_re "\\u{a}")')

    def test_flattened_literal(self):
        self.assertEqual(translate_regex_to_smtlib("ABC"), '(str.to_re "ABC")')

if __name__ == '__main__':
    unittest.main()
