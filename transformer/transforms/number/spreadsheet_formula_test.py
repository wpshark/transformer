# -*- coding: utf-8 -*-

import unittest
from decimal import Decimal

from . import spreadsheet_formula

class TestNumberSpreadsheetStyleFormulaTransform(unittest.TestCase):
    transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

    def transform(self, *args):
        return self.transformer.transform(*args)

    def test_decimal_output(self):
        operations = [
            'ABS(-5.5)',
            'PRODUCT(-2.5, -2.5)',
            'SQRT(20)',
            'POW(-2.5, 5)',
            'POWER(-2.5, 5)',
            'ROUND(INT(4.5))',
            'ROUND(2.5555, 2)',
            'ROUNDDOWN(INT(4.5), 2)',
            'ROUNDDOWN(2.5555, 2)',
            'ROUNDUP(INT(4.5), 2)',
            'ROUNDUP(2.5555, 2)',
            'RAND()',
            'RANDBETWEEN(1, 5)',
            'PI()',
            'SQRTPI(2)',
            'DEGREES(3.14)',
            'RADIANS(180)',
            'COS(180)',
            'ACOS(0.5)',
            'COSH(0.5)',
            'ACOSH(1)',
            'SIN(180)',
            'ASIN(0.5)',
            'SINH(0.5)',
            'ASINH(1)',
            'TAN(180)',
            'ATAN(0.5)',
            'ATAN2(0.5, 2)',
            'TANH(0.5)',
            'ATANH(0.5)',
            'EXP(0.5)',
            'LN(0.5)',
            'LOG(0.5, 5)',
            'LOG10(100)',
            'AVERAGE(50, 1.5, 10)',
            'MEDIAN(50, 1.5, 10)',
            'MEDIAN(50, 1.5)',
            'GEOMEAN(50, 1.5, 10)',
            'CEILING(-2.5)',
            'CEILING(-2.5, .25)',
            'FLOOR(4.3)',
            'FLOOR(-2.5, .25)',
        ]
        for operation in operations:
            transformed = self.transform(operation)
            self.assertIsInstance(
                transformed, Decimal, '%s: %r is not an instance of Decimal.' % (operation, transformed)
            )

    def test_int_output(self):
        operations = [
            'EVEN(-4.3)',
            'INT(4.5)',
            'ODD(4.3)',
            'TRUNC(4.3)',
            'FACT(5)',
            'FACTDOUBLE(5)',
        ]
        for operation in operations:
            transformed = self.transform(operation)
            self.assertIsInstance(
                transformed, (int, int), '%s: %r is not an instance of int.' % (operation, transformed)
            )
    
    def test_strip(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()
        transformer.transform('IF(AND("Mon" = "Sun", 00<20), "today at 8pm", "2am") ')
        transformer.transform(' IF(AND("Mon" = "Sun", 00<20), "today at 8pm", "2am")')
        transformer.transform(' IF(AND("Mon" = "Sun", 00<20), "today at 8pm", "2am") ')

    def test_spreadsheet_formula(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

        self.assertEqual(2, transformer.transform('1 - -1'))

        self.assertEqual(6, transformer.transform('1 + 2 + 3'))
        self.assertEqual(-4, transformer.transform('1 - 2 - 3'))
        self.assertEqual(6, transformer.transform('1 * 2 * 3'))
        self.assertEqual(
            Decimal('0.1666666666666666666666666667'),
            transformer.transform('1 / 2 / 3'),
        )

        self.assertEqual(1, transformer.transform('(1 + 2) / 3 + MIN(0, 10)'))

        self.assertEqual(1, transformer.transform('MOD(1, 2)'))
        self.assertEqual(0, transformer.transform('MOD(2, 2)'))

        self.assertEqual(Decimal('0.01'), transformer.transform('1%'))

        self.assertEqual(True, transformer.transform('MOD(2, 2) = 0'))
        self.assertEqual(True, transformer.transform('MOD(2, 2) <> 1'))
        self.assertEqual(10, transformer.transform('MAX(5, 2, 10)'))

        self.assertEqual(True, transformer.transform('5 > 0'))
        self.assertEqual(True, transformer.transform('5 >= 0'))
        self.assertEqual(False, transformer.transform('5 > 6'))
        self.assertEqual(False, transformer.transform('5 >= 6'))
        self.assertEqual(False, transformer.transform('5 < 0'))
        self.assertEqual(False, transformer.transform('5 <= 0'))
        self.assertEqual(True, transformer.transform('5 < 6'))
        self.assertEqual(True, transformer.transform('5 <= 6'))

        self.assertEqual(4, transformer.transform('POWER(2, 2)'))
        self.assertEqual(12, transformer.transform('ABS(-12)'))

        self.assertEqual(1, transformer.transform('AND(1,2)'))
        self.assertEqual(1, transformer.transform('OR(0,1)'))
        self.assertEqual(0, transformer.transform('AND(0,1)'))

        self.assertEqual(1, transformer.transform('IF(TRUE, 1, 2)'))
        self.assertEqual(2, transformer.transform('IF(FALSE, 1, 2)'))

        self.assertEqual(100, transformer.transform('=100'))

        # ROUND returns a Decimal object
        self.assertEqual(Decimal('8.39'), transformer.transform('ROUND(8.385, 2)'))

        self.assertEqual(
            Decimal('4078.715'),
            transformer.transform(
                '=(135743*(0.5/100))+(135743*(0/100))+2050+1350',
            ),
        )

    def test_unicode_strings(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

        self.assertEqual('χϩί', transformer.transform('="χϩί"'))
        self.assertEqual(True, transformer.transform('="χϩί"="χϩί"'))
        self.assertEqual('yes', transformer.transform('=IF("χϩί"="χϩί", "yes", "no")'))

    def test_invalid_formula(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

        with self.assertRaises(Exception):
            transformer.transform('1 . -1')

        with self.assertRaises(Exception):
            transformer.transform('ABND(0,1)')

    def test_empty_formula(self):
        transformer = spreadsheet_formula.NumberSpreadsheetStyleFormulaTransform()

        with self.assertRaises(Exception):
            transformer.transform(None)

        with self.assertRaises(Exception):
            transformer.transform('')
