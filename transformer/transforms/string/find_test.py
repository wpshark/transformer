import unittest
import find

from transformer.util import APIError


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
            ("baa hello", "hello", "1", 4),
        ]
        for s, f, offset, expected_pos in tests:
            self.assertEqual(transformer.transform(s, find=f, offset=offset), expected_pos)

    def test_find_offset_invalid(self):
        transformer = find.StringFindTransform()

        with self.assertRaises(APIError):
            transformer.transform("test", find="", offset=None)

        with self.assertRaises(APIError):
            transformer.transform("test", find="", offset=1.1)

        with self.assertRaises(APIError):
            transformer.transform("test", find="", offset="0a1")
