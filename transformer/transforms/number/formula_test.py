import unittest
import formula

class TestNumberFormulaTransform(unittest.TestCase):

    def test_formula(self):
        transformer = formula.NumberFormulaTransform()

        self.assertEqual(2, transformer.transform(u'1 - -1'))

        self.assertEqual(6, transformer.transform(u'1 + 2 + 3'))
        self.assertEqual(-4, transformer.transform(u'1 - 2 - 3'))
        self.assertEqual(6, transformer.transform(u'1 * 2 * 3'))
        self.assertEqual(0.16666666666666666, transformer.transform(u'1 / 2 / 3'))

        self.assertEqual(1, transformer.transform(u'(1 + 2) / 3 + MIN(0, 10)'))

        self.assertEqual(1, transformer.transform(u'MOD(1, 2)'))
        self.assertEqual(0, transformer.transform(u'MOD(2, 2)'))

        self.assertEqual(0.01, transformer.transform(u'1%'))

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

        self.assertEqual(4, transformer.transform(u'POW(2, 2)'))

        self.assertEqual(1, transformer.transform(u'AND(1,2)'))
        self.assertEqual(1, transformer.transform(u'OR(0,1)'))
        self.assertEqual(0, transformer.transform(u'AND(0,1)'))

        self.assertEqual(1, transformer.transform(u'IF(TRUE, 1, 2)'))
        self.assertEqual(2, transformer.transform(u'IF(FALSE, 1, 2)'))
