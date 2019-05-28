import unittest
import import_csv


class TestUtilImportCSVTransform(unittest.TestCase):

    def test_import_csv(self):
        transformer = import_csv.UtilImportCSVTransform()
        # UTF-8 - text
        self.assertEqual(
        {
            "csv_text": "\xc3\xb8o,\xc3\xa9e,\xc3\xbcu\n1,2,3\n4,5,6\n8,\xc3\xbcu,10\n",
            "line_items": [{"\xc3\xb8o":"1","\xc3\xa9e":"2","\xc3\xbcu":"3"},
            {"\xc3\xb8o":"4","\xc3\xa9e":"5","\xc3\xbcu":"6"},
            {"\xc3\xb8o":"8",'\xc3\xa9e':"\xc3\xbcu","\xc3\xbcu":"10"}],
            "header": True

        },
        transformer.transform('https://drive.google.com/uc?export=download&id=1R_Pr0qaIUUVNO8c0oHoFnNtJl3el86xw',True))
        # UTF-8 - line-item_
        # UTF-8 - no csv, just text
        self.assertEqual(
        {
            "csv_text": "garbage stuff here.....",
            "line_items":[],
            "header": True
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=14lvE6KkQzFvbl0bd8DOoW-12aTRUHEQH',True))
        # no headers - values missing, but all delimited
        self.assertEqual(
        {
        "csv_text": "1,2,3,4,5\n5,6,7,,8\n9,,11,,12\n,,14,15,16",
        "line_items": [
      {
        "item_1": "1",
        "item_2": "2",
        "item_3": "3",
        "item_4": "4",
        "item_5": "5"
      },
      {
        "item_1": "5",
        "item_2": "6",
        "item_3": "7",
        "item_4": "",
        "item_5": "8"
      },
      {
        "item_1": "9",
        "item_2": "",
        "item_3": "11",
        "item_4": "",
        "item_5": "12"
      },
      {
        "item_1": "",
        "item_2": "",
        "item_3": "14",
        "item_4": "15",
        "item_5": "16"
      }
      ],
        "header": False,
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=1I-t5L1KiDu4RDZCFTW2ydzJNwlfwm4Ld',False))
        # forced_header headers - values missing, but all delimited
        self.assertEqual(
        {
        "csv_text": "1,2,3,4,5\n5,6,7,,8\n9,,11,,12\n,,14,15,16",
        "line_items": [
        {
        "1": "5",
        "2": "6",
        "3": "7",
        "4": "",
        "5": "8"
        },
        {
        "1": "9",
        "2": "",
        "3": "11",
        "4": "",
        "5": "12"
        },
        {
        "1": "",
        "2": "",
        "3": "14",
        "4": "15",
        "5": "16"
      }
      ],
      "header": "forced",
      },
      transformer.transform('https://drive.google.com/uc?export=download&id=1I-t5L1KiDu4RDZCFTW2ydzJNwlfwm4Ld',True))
