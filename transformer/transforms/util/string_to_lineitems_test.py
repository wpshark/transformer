import unittest
import string_to_lineitems


class TestUtilLineItemizerTransform(unittest.TestCase):
    def test_string_to_lineitems(self):
        transformer = string_to_lineitems.UtilLineItemizerTransform()
        self.assertEqual(
            {
                "test lines": [
                    {"price": "a"},
                    {"price": "b"},
                    {"price": "c"},
                    {"price": "d"},
                ]
            },
            transformer.transform("test lines", my_dict={"price": "a,b,c,d"}),
        )
        self.assertEqual(
            {
                "Line-item(s)": [
                    {"price": "a"},
                    {"price": "b"},
                    {"price": "c"},
                    {"price": "d"},
                ]
            },
            transformer.transform("", my_dict={"price": "a,b,c,d"}),
        )
        self.assertEqual(
            {
                "Line-item(s)": [
                    {"price": "a", "name": "one"},
                    {"price": "b", "name": "two"},
                    {"price": "c", "name": "three"},
                    {"price": "d", "name": "four"},
                ]
            },
            transformer.transform(
                "", my_dict={"price": "a,b,c,d", "name": "one,two,three,four"}
            ),
        )

    def test_string_to_lineitems_variable_length(self):
        transformer = string_to_lineitems.UtilLineItemizerTransform()
        self.assertEqual(
            {
                "Line-item(s)": [
                    {"price": "a", "name": "one"},
                    {"price": "b", "name": "two"},
                    {"price": "c", "name": "three"},
                    {"price": "d"},
                ]
            },
            transformer.transform(
                "", my_dict={"price": "a,b,c,d", "name": "one,two,three"}
            ),
        )

    def test_string_to_lineitems_empty(self):
        transformer = string_to_lineitems.UtilLineItemizerTransform()
        self.assertEqual({"Line-item(s)": []}, transformer.transform("", my_dict={}))
        self.assertEqual(
            {
                "Line-item(s)": [
                    {"price": "a", "name": ""},
                    {"price": " ", "name": "two"},
                ]
            },
            transformer.transform("", my_dict={"price": "a, ", "name": ",two"}),
        )
        self.assertEqual(
            {"Line-item(s)": [{"name": "one"}, {"name": "two"}]},
            transformer.transform("", my_dict={"": "a,b", "name": "one,two"}),
        )
