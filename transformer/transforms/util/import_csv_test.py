import unittest
import import_csv


class TestUtilImportCSVTransform(unittest.TestCase):

    def test_import_csv(self):
        transformer = import_csv.UtilImportCSVTransform()
        self.assertEqual(
        {
            "CSV Text": "\xc3\xb8o,\xc3\xa9e,\xc3\xbcu\n1,2,3\n4,5,6\n8,9,10\n",
            "header": True,
            "line item output": False
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=1R_Pr0qaIUUVNO8c0oHoFnNtJl3el86xw', False))
        self.assertEqual(
        {
            "Line-item(s)": [{"\xc3\xb8o":"1","\xc3\xa9e":"2","\xc3\xbcu":"3"},
            {"\xc3\xb8o":"4","\xc3\xa9e":"5","\xc3\xbcu":"6"},
            {"\xc3\xb8o":"8","\xc3\xa9e":"9","\xc3\xbcu":"10"}],
            "header": True,
            "line item output": True
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=1R_Pr0qaIUUVNO8c0oHoFnNtJl3el86xw', True))
        self.assertEqual(
        {
            "CSV Text": "garbage stuff here.....",
            "header": True,
            "line item output": False
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=14lvE6KkQzFvbl0bd8DOoW-12aTRUHEQH', False))
        self.assertEqual(
        {
            "Line-item(s)": [],
            "header": True,
            "line item output": True
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=14lvE6KkQzFvbl0bd8DOoW-12aTRUHEQH', True))
