import unittest
import line_itemizer


class TestUtilLineItemizerTransform(unittest.TestCase):
    def test_line_itemizer(self):
        transformer = line_itemizer.UtilLineItemizerTransform()
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

    def test_line_itemizer_variable_length(self):
        transformer = line_itemizer.UtilLineItemizerTransform()
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

    def test_line_itemizer_empty(self):
        transformer = line_itemizer.UtilLineItemizerTransform()
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

    def test_line_itemizer_subtotals(self):
        transformer = line_itemizer.UtilLineItemizerTransform()
        self.assertEqual(
            {
                "test lines": [
                    {"price": "1", "qty": "1", "Subtotal": "1.00"},
                    {"price": "2", "qty": "2", "Subtotal": "4.00"},
                    {"price": "3", "qty": "3", "Subtotal": "9.00"},
                    {"price": "4", "qty": "4", "Subtotal": "16.00"},
                ]
            },
            transformer.transform(
                "test lines",
                my_dict={"price": "1,2,3,4", "qty": "1,2,3,4"},
                decimals="2",
                subtotal_toggle=True,
            ),
        )
        self.assertEqual(
            {
                "test lines": [
                    {"price": "1", "qty": "1", "Subtotal": "1.00"},
                    {"price": "2", "qty": "2", "Subtotal": "4.00"},
                    {"price": "3", "qty": "3", "Subtotal": "9.00"},
                    {"price": "4", "qty": "4", "Subtotal": "16.00"},
                ]
            },
            transformer.transform(
                "test lines",
                my_dict={"price": "1,2,3,4", "qty": "1,2,3,4", "Subtotal": "x,y,z,a"},
                decimals="2",
                subtotal_toggle=True,
            ),
        )
        self.assertEqual(
            {
                "test lines": [
                    {"price": "1", "qty": "o", "Subtotal": "x"},
                    {"price": "2", "qty": "2", "Subtotal": "4.00"},
                    {"price": "3", "qty": "3", "Subtotal": "9.00"},
                    {"price": "4", "qty": "4", "Subtotal": "16.00"},
                ]
            },
            transformer.transform(
                "test lines",
                my_dict={"price": "1,2,3,4", "qty": "o,2,3,4", "Subtotal": "x,y,z,a"},
                decimals="2",
                subtotal_toggle=True,
            ),
        )
        self.assertEqual(
            {
                "test lines": [
                    {"price": "1", "qty": "1"},
                    {"price": "2", "qty": "2"},
                    {"price": "3", "qty": "3"},
                    {"price": "4", "qty": "4"},
                ]
            },
            transformer.transform(
                "test lines",
                my_dict={"price": "1,2,3,4", "qty": "1,2,3,4"},
                decimals="2",
                subtotal_toggle=False,
            ),
        )
