import unittest
from re2smtlib import translate_regex_to_smtlib

class TestBasic(unittest.TestCase):
    def test_single_literal(self):
        self.assertEqual(translate_regex_to_smtlib("X"), '(str.to_re "X")')

    def test_escape_character(self):
        self.assertEqual(translate_regex_to_smtlib("\n"), '(str.to_re "\\u{a}")')

    def test_flattened_literal(self):
        self.assertEqual(translate_regex_to_smtlib("ABC"), '(str.to_re "ABC")')

    def test_star_literal(self):
        self.assertEqual(translate_regex_to_smtlib("a*"), '(re.* (str.to_re "a"))')

    def test_plus_literal(self):
        self.assertEqual(translate_regex_to_smtlib("a+"), '(re.+ (str.to_re "a"))')

    def test_parens(self):
        self.assertEqual(translate_regex_to_smtlib("(a)"), '(str.to_re "a")')

    def test_union(self):
        self.assertEqual(translate_regex_to_smtlib("a|b"), '(re.union (str.to_re "a") (str.to_re "b"))')

    def test_union_of_long_literals(self):
        self.assertEqual(translate_regex_to_smtlib("(abc)|d"), '(re.union (str.to_re "abc") (str.to_re "d"))')

    def test_negated_character_class(self):
        self.assertEqual(translate_regex_to_smtlib("[^a]"), '(re.comp (str.to_re "a"))')

    def test_optional(self):
        self.assertEqual(translate_regex_to_smtlib("a?"), '(re.opt (str.to_re "a"))')

    def test_minimum_bounded_repeat(self):
        self.assertEqual(translate_regex_to_smtlib("a{5,}"), '(re.++ ((_ re.loop 5 5) (str.to_re "a")) (re.* (str.to_re "a")))')

    def test_single_argument_union(self):
        self.assertEqual(translate_regex_to_smtlib("a|$"), '(str.to_re "a")')

if __name__ == '__main__':
    unittest.main()
