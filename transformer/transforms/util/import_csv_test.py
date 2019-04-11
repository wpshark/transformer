import unittest
import import_csv


class TestUtilImportCSVTransform(unittest.TestCase):

    def test_import_csv(self):
        transformer = import_csv.UtilImportCSVTransform()
        self.assertEqual(
        {
            "CSV Text": "\xc3\xb8o,\xc3\xa9e,\xc3\xbcu\n1,2,3\n4,5,6\n8,9,10\n",
            "filesize": "0K",
            "header": True,
            "line item output": False
        },
        transformer.transform('https://drive.google.com/uc?export=download&id=1R_Pr0qaIUUVNO8c0oHoFnNtJl3el86xw', False))
