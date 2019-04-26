import unittest
import import_csv


class TestUtilImportCSVTransform(unittest.TestCase):

    def test_import_csv(self):
        transformer = import_csv.UtilImportCSVTransform()
        # UTF-8 - text
        self.assertEqual(
        {
            "CSV Text": "\xc3\xb8o,\xc3\xa9e,\xc3\xbcu\n1,2,3\n4,5,6\n8,\xc3\xbcu,10\n",
            "header": True,
            "line-item output": False
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=1R_Pr0qaIUUVNO8c0oHoFnNtJl3el86xw', False))
        # UTF-8 - line-item
        self.assertEqual(
        {
            "Line-item(s)": [{"\xc3\xb8o":"1","\xc3\xa9e":"2","\xc3\xbcu":"3"},
            {"\xc3\xb8o":"4","\xc3\xa9e":"5","\xc3\xbcu":"6"},
            {"\xc3\xb8o":"8",'\xc3\xa9e':"\xc3\xbcu","\xc3\xbcu":"10"}],
            "header": True,
            "line-item output": True
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=1R_Pr0qaIUUVNO8c0oHoFnNtJl3el86xw', True))
        # UTF-8 - no csv, just text
        self.assertEqual(
        {
            "CSV Text": "garbage stuff here.....",
            "header": True,
            "line-item output": False
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=14lvE6KkQzFvbl0bd8DOoW-12aTRUHEQH', False))
        # UTF-8 - no csv, just text
        self.assertEqual(
        {
            "Line-item(s)": [],
            "header": True,
            "line-item output": True
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=14lvE6KkQzFvbl0bd8DOoW-12aTRUHEQH', True))
        # no headers - values missing, but all delimited
        self.assertEqual(
        {"Line-item(s)": [
      {
        "Item 1": "3",
        "Item 2": "2",
        "Item 3": "1",
        "Item 4": "5",
        "Item 5": "4"
      },
      {
        "Item 1": "7",
        "Item 2": "6",
        "Item 3": "5",
        "Item 4": "8",
        "Item 5": ""
      },
      {
        "Item 1": "11",
        "Item 2": "",
        "Item 3": "9",
        "Item 4": "12",
        "Item 5": ""
      },
      {
        "Item 1": "14",
        "Item 2": "",
        "Item 3": "",
        "Item 4": "16",
        "Item 5": "15"
      }
    ],
    "header": False,
    "line-item output": True
  },
    transformer.transform('https://drive.google.com/uc?export=download&id=1I-t5L1KiDu4RDZCFTW2ydzJNwlfwm4Ld', True))
