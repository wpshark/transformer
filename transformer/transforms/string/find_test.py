import unittest
import find


class TestStringFindTransform(unittest.TestCase):
    def test_find(self):
        transformer = find.StringFindTransform()

        tests = [
            ("", "", -1),
            ("", None, -1),
            ("", "a", -1),
            ("a", "a", 0),
            ("aa", "a", 0),
            ("baa", "a", 1),
            ("baa hello", "hello", 4),
        ]
        for s, f, expected_pos in tests:
            self.assertEqual(transformer.transform(s, find=f), expected_pos)

    def test_find_offset(self):
        transformer = find.StringFindTransform()

        tests = [
            ("", "", 1, -1),
            ("", None, 1, -1),
            ("", "a", 1, -1),
            ("a", "a", 0, 0),
            ("a", "a", 1, -1),
            ("aa", "a", 1, 1),
            ("baa", "a", 1, 1),
            ("baa", "a", 2, 2),
            ("baa hello", "hello", 1, 4),
            ("baa hello", "hello", 5, -1),
        ]
        for s, f, offset, expected_pos in tests:
            self.assertEqual(transformer.transform(s, find=f, offset=offset), expected_pos)
