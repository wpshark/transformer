import unittest
import lineitem_to_string_v2


class TestUtilLineItemToStringV2Transform(unittest.TestCase):
    def test_lineitem_to_string_v2_empty(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()

        self.assertEqual(
            {"text": "", "item 1": ""},
            transformer.transform_many([], options={"separator": ","}),
        )
        self.assertEqual(
            {"text": "", "item 1": ""},
            transformer.transform_many([""], options={"separator": ","}),
        )
        self.assertEqual(
            {"text": "", "item 1": ""}, transformer.transform_many("")
        )

    def test_lineitem_to_string_v2_many_empty(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()

        self.assertEqual(
            {"text": ",c,d", "item 1": "", "item 2": "c", "item 3": "d"},
            transformer.transform_many(["", "c", "d"], options={"separator": ","}),
        )
        self.assertEqual(
            {"text": ",,c,d", "item 1": "", "item 2": "", "item 3": "c,d"},
            transformer.transform_many(["", "", "c,d"], options={"separator": ","}),
        )
        self.assertEqual(
            {"text": ",", "item 1": "", "item 2": ""},
            transformer.transform_many(["", ""], options={"separator": ","}),
        )
        self.assertEqual(
            {"text": "c,d,", "item 1": "c", "item 2": "d", "item 3": ""},
            transformer.transform_many(["c", "d", ""], options={"separator": ","}),
        )

    def test_lineitem_to_string_v2_one(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual(
            {"text": "a", "item 1": "a"},
            transformer.transform_many(["a"], options={"separator": ","}),
        )

    def test_lineitem_to_string_v2_many(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual(
            {"text": "a,b,c,d", "item 1": "a,b", "item 2": "c,d"},
            transformer.transform_many(["a,b", "c,d"], options={"separator": ","}),
        )
        self.assertEqual(
            {
                "text": "a,b,c,d",
                "item 1": "a",
                "item 2": "b",
                "item 3": "c",
                "item 4": "d",
            },
            transformer.transform_many(
                ["a", "b", "c", "d"], options={"separator": ","}
            ),
        )
        self.assertEqual(
            {"text": "a,b,c,d", "item 1": "a,b,c,d"},
            transformer.transform_many(["a,b,c,d"], options={"separator": ","}),
        )

    def test_lineitem_to_string_v2_other_separator(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual(
            {
                "text": "a b c d",
                "item 1": "a",
                "item 2": "b",
                "item 3": "c",
                "item 4": "d",
            },
            transformer.transform_many(
                ["a", "b", "c", "d"], options={"separator": "[:space:]"}
            ),
        )
        self.assertEqual(
            {
                "text": "a b c d",
                "item 1": "a",
                "item 2": "b",
                "item 3": "c",
                "item 4": "d",
            },
            transformer.transform_many(
                ["a", "b", "c", "d"], options={"separator": "[:s:]"}
            ),
        )
        self.assertEqual(
            {
                "text": "a;b;c;d",
                "item 1": "a",
                "item 2": "b",
                "item 3": "c",
                "item 4": "d",
            },
            transformer.transform_many(
                ["a", "b", "c", "d"], options={"separator": ";"}
            ),
        )

    def test_lineitem_to_string_v2_nolineitem(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual(
            {"text": "abcd", "item 1": "abcd"},
            transformer.transform_many("abcd", options={"separator": "[:space:]"}),
        )
