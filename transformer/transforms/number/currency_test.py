# -*- coding: utf-8 -*-
import unittest
from . import currency

class TestNumberCurrencyTransform(unittest.TestCase):
    def test_currency(self):
        transformer = currency.NumberCurrencyTransform()
        self.assertEqual('$1,234.10 USD', transformer.transform(1234.1))
        self.assertEqual('\xa31,234.10 GBP', transformer.transform(1234.1, currency='GBP'))
        self.assertEqual('\u20ac1,234.10 EUR', transformer.transform(1234.1, currency='EUR'))
        self.assertEqual('\u20ac1.234,10 EUR', transformer.transform(1234.1, currency='EUR', currency_locale='es_ES'))
        self.assertEqual('\u20ac1.234,10 EUR', transformer.transform(1234.1, currency='EUR', currency_locale='es-ES'))
        self.assertEqual('\u20ac1.234,10', transformer.transform(1234.1, currency='EUR', currency_format='¤#,##0.00', currency_locale='es-ES'))
        self.assertEqual('CA$1.234,10', transformer.transform(1234.1, currency='CAD', currency_format='¤#,##0.00', currency_locale='es-ES'))
        self.assertEqual('CA$1,234.10', transformer.transform(1234.1, currency='CAD', currency_format='¤#,##0.00', currency_locale='en-US'))
        self.assertEqual('Something', transformer.transform('Something', currency='CAD', currency_format='¤#,##0.00', currency_locale='en-US'))
        self.assertEqual('', transformer.transform(None, currency='CAD', currency_format='¤#,##0.00', currency_locale='en-US'))
        self.assertEqual('', transformer.transform('', currency='CAD', currency_format='¤#,##0.00', currency_locale='en-US'))
