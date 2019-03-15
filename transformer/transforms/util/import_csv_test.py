import unittest
import import_csv


class TestUtilImportCSVTransform(unittest.TestCase):

    def test_import_csv(self):
        transformer = import_csv.UtilImportCSVTransform()

        #self.assertEqual('', transformer.transform([''], options={'line_item':0}))
