import unittest
from . import lineitem_to_string_v2


class TestUtilLineItemToStringV2Transform(unittest.TestCase):
    def test_lineitem_to_string_v2_empty(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()

        self.assertEqual(
            {"text": "", "item_1": "", "item_last": ""},
            transformer.transform_many([], options={"separator": ","}),
        )
        self.assertEqual(
            {"text": "", "item_1": "", "item_last": ""},
            transformer.transform_many([""], options={"separator": ","}),
        )
        self.assertEqual(
            {"text": "", "item_1": "", "item_last": ""}, transformer.transform_many("")
        )

    def test_lineitem_to_string_v2_many_empty(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()

        self.assertEqual(
            {
                "text": ",c,d",
                "item_1": "",
                "item_2": "c",
                "item_3": "d",
                "item_last": "d",
            },
            transformer.transform_many(["", "c", "d"], options={"separator": ","}),
        )
        self.assertEqual(
            {
                "text": ",,c,d",
                "item_1": "",
                "item_2": "",
                "item_3": "c,d",
                "item_last": "c,d",
            },
            transformer.transform_many(["", "", "c,d"], options={"separator": ","}),
        )
        self.assertEqual(
            {"text": ",", "item_1": "", "item_2": "", "item_last": ""},
            transformer.transform_many(["", ""], options={"separator": ","}),
        )
        self.assertEqual(
            {
                "text": "c,d,",
                "item_1": "c",
                "item_2": "d",
                "item_3": "",
                "item_last": "",
            },
            transformer.transform_many(["c", "d", ""], options={"separator": ","}),
        )

    def test_lineitem_to_string_v2_one(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual(
            {"text": "a", "item_1": "a", "item_last": "a"},
            transformer.transform_many(["a"], options={"separator": ","}),
        )

    def test_lineitem_to_string_v2_many(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual(
            {"text": "a,b,c,d", "item_1": "a,b", "item_2": "c,d", "item_last": "c,d"},
            transformer.transform_many(["a,b", "c,d"], options={"separator": ","}),
        )
        self.assertEqual(
            {
                "text": "a,b,c,d",
                "item_1": "a",
                "item_2": "b",
                "item_3": "c",
                "item_4": "d",
                "item_last": "d",
            },
            transformer.transform_many(
                ["a", "b", "c", "d"], options={"separator": ","}
            ),
        )
        self.assertEqual(
            {"text": "a,b,c,d", "item_1": "a,b,c,d", "item_last": "a,b,c,d"},
            transformer.transform_many(["a,b,c,d"], options={"separator": ","}),
        )

    def test_lineitem_to_string_v2_other_separator(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual(
            {
                "text": "a b c d",
                "item_1": "a",
                "item_2": "b",
                "item_3": "c",
                "item_4": "d",
                "item_last": "d",
            },
            transformer.transform_many(
                ["a", "b", "c", "d"], options={"separator": "[:space:]"}
            ),
        )
        self.assertEqual(
            {
                "text": "a b c d",
                "item_1": "a",
                "item_2": "b",
                "item_3": "c",
                "item_4": "d",
                "item_last": "d",
            },
            transformer.transform_many(
                ["a", "b", "c", "d"], options={"separator": "[:s:]"}
            ),
        )
        self.assertEqual(
            {
                "text": "a;b;c;d",
                "item_1": "a",
                "item_2": "b",
                "item_3": "c",
                "item_4": "d",
                "item_last": "d",
            },
            transformer.transform_many(
                ["a", "b", "c", "d"], options={"separator": ";"}
            ),
        )

    def test_lineitem_to_string_v2_nolineitem(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual(
            {"text": "abcd", "item_1": "abcd", "item_last": "abcd"},
            transformer.transform_many("abcd", options={"separator": "[:space:]"}),
        )
