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
                    {"price": "1", "qty": "1", "subtotal": "1.00"},
                    {"price": "2", "qty": "2", "subtotal": "4.00"},
                    {"price": "3", "qty": "3", "subtotal": "9.00"},
                    {"price": "4", "qty": "4", "subtotal": "16.00"},
                ]
            },
            transformer.transform(
                "test lines",
                my_dict={"price": "1,2,3,4", "qty": "1,2,3,4"},
                my_price="price",
                my_qty="qty",
                my_subtotal_name="subtotal",
                my_decimals="2",
                my_subtotal_toggle="Yes",
            ),
        )
        self.assertEqual(
            {
                "test lines": [
                    {"price": "1", "qty": "1", "subtotal": "x"},
                    {"price": "2", "qty": "2", "subtotal": "y"},
                    {"price": "3", "qty": "3", "subtotal": "z"},
                    {"price": "4", "qty": "4", "subtotal": "a"},
                ]
            },
            transformer.transform(
                "test lines",
                my_dict={"price": "1,2,3,4", "qty": "1,2,3,4", "subtotal": "x,y,z,a"},
                my_price="price",
                my_qty="qty",
                my_subtotal_name="subtotal",
                my_decimals="2",
                my_subtotal_toggle="Yes",
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
                my_price="price",
                my_qty="qty",
                my_subtotal_name="subtotal",
                my_decimals="2",
                my_subtotal_toggle="No",
            ),
        )

    def test_line_itemizer_numbering(self):
        transformer = line_itemizer.UtilLineItemizerTransform()
        self.assertEqual(
            {
                "test lines": [
                    {"price": "1", "qty": "1", "number": "1"},
                    {"price": "2", "qty": "2", "number": "2"},
                    {"price": "3", "qty": "3", "number": "3"},
                    {"price": "4", "qty": "4", "number": "4"},
                ]
            },
            transformer.transform(
                "test lines",
                my_dict={"price": "1,2,3,4", "qty": "1,2,3,4"},
                my_numbering_name="number",
                my_numbering_toggle="Yes",
            ),
        )
        self.assertEqual(
            {
                "test lines": [
                    {"price": "1", "qty": "1", "number": "x"},
                    {"price": "2", "qty": "2", "number": "y"},
                    {"price": "3", "qty": "3", "number": "z"},
                    {"price": "4", "qty": "4", "number": "a"},
                ]
            },
            transformer.transform(
                "test lines",
                my_dict={"price": "1,2,3,4", "qty": "1,2,3,4", "number": "x,y,z,a"},
                my_numbering_name="number",
                my_numbering_toggle="Yes",
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
                my_numbering_name="number",
                my_numbering_toggle="No",
            ),
        )
