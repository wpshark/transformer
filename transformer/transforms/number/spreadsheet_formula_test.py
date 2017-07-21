# -*- coding: utf-8 -*-

import unittest
from decimal import Decimal

import spreadsheet_formula

class TestNumberSpreadsheetStyleFormulaTransform(unittest.TestCase):

    def test_spreadsheet_formula(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

        self.assertEqual(2, transformer.transform(u'1 - -1'))

        self.assertEqual(6, transformer.transform(u'1 + 2 + 3'))
        self.assertEqual(-4, transformer.transform(u'1 - 2 - 3'))
        self.assertEqual(6, transformer.transform(u'1 * 2 * 3'))
        self.assertEqual(
            Decimal('0.1666666666666666666666666667'),
            transformer.transform(u'1 / 2 / 3'),
        )

        self.assertEqual(1, transformer.transform(u'(1 + 2) / 3 + MIN(0, 10)'))

        self.assertEqual(1, transformer.transform(u'MOD(1, 2)'))
        self.assertEqual(0, transformer.transform(u'MOD(2, 2)'))

        self.assertEqual(Decimal('0.01'), transformer.transform(u'1%'))

        self.assertEqual(True, transformer.transform(u'MOD(2, 2) = 0'))
        self.assertEqual(True, transformer.transform(u'MOD(2, 2) <> 1'))
        self.assertEqual(10, transformer.transform(u'MAX(5, 2, 10)'))

        self.assertEqual(True, transformer.transform(u'5 > 0'))
        self.assertEqual(True, transformer.transform(u'5 >= 0'))
        self.assertEqual(False, transformer.transform(u'5 > 6'))
        self.assertEqual(False, transformer.transform(u'5 >= 6'))
        self.assertEqual(False, transformer.transform(u'5 < 0'))
        self.assertEqual(False, transformer.transform(u'5 <= 0'))
        self.assertEqual(True, transformer.transform(u'5 < 6'))
        self.assertEqual(True, transformer.transform(u'5 <= 6'))

        self.assertEqual(4, transformer.transform(u'POWER(2, 2)'))
        self.assertEqual(12, transformer.transform(u'ABS(-12)'))

        self.assertEqual(1, transformer.transform(u'AND(1,2)'))
        self.assertEqual(1, transformer.transform(u'OR(0,1)'))
        self.assertEqual(0, transformer.transform(u'AND(0,1)'))

        self.assertEqual(1, transformer.transform(u'IF(TRUE, 1, 2)'))
        self.assertEqual(2, transformer.transform(u'IF(FALSE, 1, 2)'))

        self.assertEqual(100, transformer.transform(u'=100'))

        # ROUND returns a Decimal object
        self.assertEqual(Decimal('8.39'), transformer.transform(u'ROUND(8.385, 2)'))

        self.assertEqual(
            Decimal('4078.715'),
            transformer.transform(
                u'=(135743*(0.5/100))+(135743*(0/100))+2050+1350',
            ),
        )

    def test_unicode_strings(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

        self.assertEqual(u'χϩί', transformer.transform(u'="χϩί"'))
        self.assertEqual(True, transformer.transform(u'="χϩί"="χϩί"'))
        self.assertEqual(u'yes', transformer.transform(u'=IF("χϩί"="χϩί", "yes", "no")'))

    def test_invalid_formula(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

        with self.assertRaises(Exception):
            transformer.transform(u'1 . -1')

        with self.assertRaises(Exception):
            transformer.transform(u'ABND(0,1)')

    def test_empty_formula(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

        with self.assertRaises(Exception):
            transformer.transform(None)

        with self.assertRaises(Exception):
            transformer.transform('')
