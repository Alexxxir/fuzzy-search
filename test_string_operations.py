import unittest
from string_operations import split_line,\
    levenshtein_distance, count_max_number_types, compare_strings
from constants import MatchingLines


class TestSplitLine(unittest.TestCase):
    def test_split_line(self):
        self.assertEqual(list(split_line("", {'a'})), [])
        self.assertEqual(list(split_line("a a", {''})), [])
        self.assertEqual(list(split_line("aba", {'a'})), [('a', 1), ('a', 3)])
        self.assertEqual(list(split_line("aba", {'a', 'b'})), [('aba', 1)])
        self.assertEqual(list(split_line("a a", {'a'})), [('a', 1), ('a', 3)])


class TestLevenshteinDistance(unittest.TestCase):
    def test_zero_length(self):
        self.assertEqual(levenshtein_distance(
            "", ""), 0)
        self.assertEqual(levenshtein_distance(
            "", "a"), 1)
        self.assertEqual(levenshtein_distance(
            "", "aaaaa"), 5)
        self.assertEqual(levenshtein_distance(
            "a", ""), 1)

    def test_equal_strings(self):
        self.assertEqual(levenshtein_distance(
            "a", "a"), 0)
        self.assertEqual(levenshtein_distance(
            "a" * 1000, "a" * 1000), 0)

    def test_not_equal_strings(self):
        self.assertEqual(levenshtein_distance(
            "a", "b"), 1)
        self.assertEqual(levenshtein_distance(
            "a" * 100, "b" * 100), 100)
        self.assertEqual(levenshtein_distance(
            "b" + "a" * 100, "a" * 100), 1)
        self.assertEqual(levenshtein_distance(
            "a", "bdd"), 3)
        self.assertEqual(levenshtein_distance(
            "a", "bad"), 2)
        self.assertEqual(levenshtein_distance(
            "abc", "def"), 3)
        self.assertEqual(levenshtein_distance(
            "abc", "bba"), 2)


class TestCompareStrings(unittest.TestCase):
    def test_count_max_number_types(self):
        self.assertEqual(count_max_number_types(0, 1, 111), 0)

        self.assertEqual(count_max_number_types(100, 10, 10), 10)
        self.assertEqual(count_max_number_types(100, 1, 10), 10)

        self.assertEqual(count_max_number_types(50, 1, 1), 0)
        self.assertEqual(count_max_number_types(50, 2, 2), 1)
        self.assertEqual(count_max_number_types(50, 3, 3), 1)
        self.assertEqual(count_max_number_types(50, 5, 5), 2)
        self.assertEqual(count_max_number_types(50, 6, 6), 3)

    def test_compare_strings_without_types(self):
        self.assertEqual(compare_strings(0, 'a', 'b'),
                         MatchingLines.MISMATCH)
        self.assertEqual(compare_strings(0, 'a', 'a'),
                         MatchingLines.FULL_MATCH)

    def test_compare_strings_unlimited_types(self):
        self.assertEqual(compare_strings(
            100, '', 'bаsdgsdg'), MatchingLines.POSSIBLE_TYPOS)
        self.assertEqual(compare_strings(
            100, 'qwertyuuiiop', 'bаsdgsdg'), MatchingLines.POSSIBLE_TYPOS)
        self.assertEqual(compare_strings(
            100, 'bаsdgsdg', 'bаsdgsdg'), MatchingLines.FULL_MATCH)

    def test_compare_strings_with_types(self):
        self.assertEqual(compare_strings(
            50, 'aaaaa', 'aaaab'),
            MatchingLines.POSSIBLE_TYPOS)
        self.assertEqual(compare_strings(
            50, 'aaaaaa', 'aababb'),
            MatchingLines.POSSIBLE_TYPOS)
        self.assertEqual(compare_strings(
            50, 'aaaaaa', 'aaaaaa'),
            MatchingLines.FULL_MATCH)
        self.assertEqual(compare_strings(
            50, 'aaaaa', 'aaaaaa'),
            MatchingLines.POSSIBLE_TYPOS)


if __name__ == '__main__':
    unittest.main()
