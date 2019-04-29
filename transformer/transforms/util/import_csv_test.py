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
        transformer.transform('https://drive.google.com/uc?export=download&id=1R_Pr0qaIUUVNO8c0oHoFnNtJl3el86xw'))
        # UTF-8 - line-item_
        # UTF-8 - no csv, just text
        self.assertEqual(
        {
            "csv_text": "garbage stuff here.....",
            "line_items":[],
            "header": True
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=14lvE6KkQzFvbl0bd8DOoW-12aTRUHEQH'))
        # no headers - values missing, but all delimited
        self.assertEqual(
        {
        "csv_text": "1,2,3,4,5\n5,6,7,,8\n9,,11,,12\n,,14,15,16",
        "line_items": [{
        "item_4": "1",
        "item_5": "2",
        "item_2": "3",
        "item_3": "4",
        "item_1": "5"
      }, {
        "item_4": "5",
        "item_5": "6",
        "item_2": "7",
        "item_3": "",
        "item_1": "8"
      }, {
        "item_4": "9",
        "item_5": "",
        "item_2": "11",
        "item_3": "",
        "item_1": "12"
      }, {
        "item_4": "",
        "item_5": "",
        "item_2": "14",
        "item_3": "15",
        "item_1": "16"
      }],
    "header": False,
  },
    transformer.transform('https://drive.google.com/uc?export=download&id=1I-t5L1KiDu4RDZCFTW2ydzJNwlfwm4Ld'))
