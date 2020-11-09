# -*- coding: utf-8 -*-
import money

from transformer.registry import register
from transformer.transforms.base import BaseTransform


class NumberCurrencyTransform(BaseTransform):

    category = 'number'
    name = 'currency'
    label = 'Format Currency'
    help_text = 'Format a number as a currency.'

    noun = 'Number'
    verb = 'format as a currency'

    def transform(self, currency_input, currency='USD', currency_locale='en_US', currency_format='¤#,##0.00 ¤¤'):
        if currency_input is None:
            return ''

        try:
            m = money.Money(currency_input, currency)
        except ValueError:
            # Return original input if we can't do anything with it
            return currency_input

        currency_locale = currency_locale.replace('-', '_') # make sure to use the babel locale format
        return m.format(currency_locale, currency_format)

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'currency',
                'label': 'Currency',
                'choices': ','.join([
                    '{}|{}'.format(code, name) for code, name in list_currencies()
                ]),
                'help_text': 'Specify the currency to be used for formatting'
            },
            {
                'type': 'unicode',
                'required': True,
                'key': 'currency_locale',
                'label': 'Currency Locale',
                'choices': ','.join([
                    '{}|{}'.format(code, name) for code, name in list_locales()
                ]),
                'help_text': 'Specify the locale to be used for the currency formatting.',
                'default': 'en_US'
            },
            {
                'type': 'unicode',
                'required': True,
                'key': 'currency_format',
                'label': 'Currency Format',
                'help_text': (
                    'Specify the format to be used for the currency formatting. '
                    'Use the unicode currency symbol (¤) for special formatting options. '
                    'Formatting rules can be found here: http://www.unicode.org/reports/tr35/tr35-numbers.html#Number_Format_Patterns'
                ),
                'choices': [
                    '¤#,##0.00',
                    '¤#,##0.00 ¤¤',
                    '¤#,##0.00 ¤¤¤',
                    '¤###0.00',
                    '#,##0.00',
                    '###0.00',
                ],
                'default': '¤#,##0.00'
            },
        ]


def list_locales():
    return [
        ('en_US', 'English (United States)'),
        ('es_US', 'Spanish (United States)'),
        ('en_GB', 'English (United Kingdom)'),
        ('es_ES', 'Spanish (Spain)'),
        ('de_DE', 'German (Germany)'),
        ('fr_FR', 'French (France)'),
        ('zh_CN', 'Chinese (Simplified)'),
        ('ru_RU', 'Russian (Russia)'),
        ('bn_IN', 'Bengali (India)'),
        ('da_DK', 'Danish (Denmark)'),
    ]


def list_currencies():
    return [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('INR', 'Indian Rupee'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('SGD', 'Singapore Dollar'),
        ('CHF', 'Swiss Franc'),
        ('MYR', 'Malaysian Ringgit'),
        ('JPY', 'Japanese Yen'),
        ('CNY', 'Chinese Yuan Renminbi'),
        ('NZD', 'New Zealand Dollar'),
        ('THB', 'Thai Baht'),
        ('HUF', 'Hungarian Forint'),
        ('AED', 'Emirati Dirham'),
        ('HKD', 'Hong Kong Dollar'),
        ('MXN', 'Mexican Peso'),
        ('ZAR', 'South African Rand'),
        ('PHP', 'Philippine Peso'),
        ('SEK', 'Swedish Krona'),
        ('IDR', 'Indonesian Rupiah'),
        ('SAR', 'Saudi Arabian Riyal'),
        ('BRL', 'Brazilian Real'),
        ('TRY', 'Turkish Lira'),
        ('KES', 'Kenyan Shilling'),
        ('KRW', 'South Korean Won'),
        ('EGP', 'Egyptian Pound'),
        ('IQD', 'Iraqi Dinar'),
        ('NOK', 'Norwegian Krone'),
        ('KWD', 'Kuwaiti Dinar'),
        ('RUB', 'Russian Ruble'),
        ('DKK', 'Danish Krone'),
        ('PKR', 'Pakistani Rupee'),
        ('ILS', 'Israeli Shekel'),
        ('PLN', 'Polish Zloty'),
        ('QAR', 'Qatari Riyal'),
        ('XAU', 'Gold Ounce'),
        ('OMR', 'Omani Rial'),
        ('COP', 'Colombian Peso'),
        ('CLP', 'Chilean Peso'),
        ('TWD', 'Taiwan New Dollar'),
        ('ARS', 'Argentine Peso'),
        ('CZK', 'Czech Koruna'),
        ('VND', 'Vietnamese Dong'),
        ('MAD', 'Moroccan Dirham'),
        ('JOD', 'Jordanian Dinar'),
        ('BHD', 'Bahraini Dinar'),
        ('XOF', 'CFA Franc'),
        ('LKR', 'Sri Lankan Rupee'),
        ('UAH', 'Ukrainian Hryvnia'),
        ('NGN', 'Nigerian Naira'),
        ('TND', 'Tunisian Dinar'),
        ('UGX', 'Ugandan Shilling'),
        ('RON', 'Romanian New Leu'),
        ('BDT', 'Bangladeshi Taka'),
        ('PEN', 'Peruvian Nuevo Sol'),
        ('GEL', 'Georgian Lari'),
        ('XAF', 'Central African CFA Franc BEAC'),
        ('FJD', 'Fijian Dollar'),
        ('VEF', 'Venezuelan Bolivar'),
        ('BYR', 'Belarusian Ruble'),
        ('HRK', 'Croatian Kuna'),
        ('UZS', 'Uzbekistani Som'),
        ('BGN', 'Bulgarian Lev'),
        ('DZD', 'Algerian Dinar'),
        ('IRR', 'Iranian Rial'),
        ('DOP', 'Dominican Peso'),
        ('ISK', 'Icelandic Krona'),
        ('XAG', 'Silver Ounce'),
        ('CRC', 'Costa Rican Colon'),
        ('SYP', 'Syrian Pound'),
        ('LYD', 'Libyan Dinar'),
        ('JMD', 'Jamaican Dollar'),
        ('MUR', 'Mauritian Rupee'),
        ('GHS', 'Ghanaian Cedi'),
        ('AOA', 'Angolan Kwanza'),
        ('UYU', 'Uruguayan Peso'),
        ('AFN', 'Afghan Afghani'),
        ('LBP', 'Lebanese Pound'),
        ('XPF', 'CFP Franc'),
        ('TTD', 'Trinidadian Dollar'),
        ('TZS', 'Tanzanian Shilling'),
        ('ALL', 'Albanian Lek'),
        ('XCD', 'East Caribbean Dollar'),
        ('GTQ', 'Guatemalan Quetzal'),
        ('NPR', 'Nepalese Rupee'),
        ('BOB', 'Bolivian Boliviano'),
        ('ZWD', 'Zimbabwean Dollar'),
        ('BBD', 'Barbadian or Bajan Dollar'),
        ('CUC', 'Cuban Convertible Peso'),
        ('LAK', 'Lao or Laotian Kip'),
        ('BND', 'Bruneian Dollar'),
        ('BWP', 'Botswana Pula'),
        ('HNL', 'Honduran Lempira'),
        ('PYG', 'Paraguayan Guarani'),
        ('ETB', 'Ethiopian Birr'),
        ('NAD', 'Namibian Dollar'),
        ('PGK', 'Papua New Guinean Kina'),
        ('SDG', 'Sudanese Pound'),
        ('MOP', 'Macau Pataca'),
        ('NIO', 'Nicaraguan Cordoba'),
        ('BMD', 'Bermudian Dollar'),
        ('KZT', 'Kazakhstani Tenge'),
        ('PAB', 'Panamanian Balboa'),
        ('BAM', 'Bosnian Convertible Marka'),
        ('GYD', 'Guyanese Dollar'),
        ('YER', 'Yemeni Rial'),
        ('MGA', 'Malagasy Ariary'),
        ('KYD', 'Caymanian Dollar'),
        ('MZN', 'Mozambican Metical'),
        ('RSD', 'Serbian Dinar'),
        ('SCR', 'Seychellois Rupee'),
        ('AMD', 'Armenian Dram'),
        ('SBD', 'Solomon Islander Dollar'),
        ('AZN', 'Azerbaijani New Manat'),
        ('SLL', 'Sierra Leonean Leone'),
        ('TOP', 'Tongan Pa\'anga'),
        ('BZD', 'Belizean Dollar'),
        ('MWK', 'Malawian Kwacha'),
        ('GMD', 'Gambian Dalasi'),
        ('BIF', 'Burundian Franc'),
        ('SOS', 'Somali Shilling'),
        ('HTG', 'Haitian Gourde'),
        ('GNF', 'Guinean Franc'),
        ('MVR', 'Maldivian Rufiyaa'),
        ('MNT', 'Mongolian Tughrik'),
        ('CDF', 'Congolese Franc'),
        ('STD', 'Sao Tomean Dobra'),
        ('TJS', 'Tajikistani Somoni'),
        ('KPW', 'North Korean Won'),
        ('MMK', 'Burmese Kyat'),
        ('LSL', 'Basotho Loti'),
        ('LRD', 'Liberian Dollar'),
        ('KGS', 'Kyrgyzstani Som'),
        ('GIP', 'Gibraltar Pound'),
        ('XPT', 'Platinum Ounce'),
        ('MDL', 'Moldovan Leu'),
        ('CUP', 'Cuban Peso'),
        ('KHR', 'Cambodian Riel'),
        ('MKD', 'Macedonian Denar'),
        ('VUV', 'Ni-Vanuatu Vatu'),
        ('MRO', 'Mauritanian Ouguiya'),
        ('ANG', 'Dutch Guilder'),
        ('SZL', 'Swazi Lilangeni'),
        ('CVE', 'Cape Verdean Escudo'),
        ('SRD', 'Surinamese Dollar'),
        ('XPD', 'Palladium Ounce'),
        ('SVC', 'Salvadoran Colon'),
        ('BSD', 'Bahamian Dollar'),
        ('XDR', 'IMF Special Drawing Rights'),
        ('RWF', 'Rwandan Franc'),
        ('AWG', 'Aruban or Dutch Guilder'),
        ('DJF', 'Djiboutian Franc'),
        ('BTN', 'Bhutanese Ngultrum'),
        ('KMF', 'Comoran Franc'),
        ('WST', 'Samoan Tala'),
        ('SPL', 'Seborgan Luigino'),
        ('ERN', 'Eritrean Nakfa'),
        ('FKP', 'Falkland Island Pound'),
        ('SHP', 'Saint Helenian Pound'),
        ('JEP', 'Jersey Pound'),
        ('TMT', 'Turkmenistani Manat'),
        ('TVD', 'Tuvaluan Dollar'),
        ('IMP', 'Isle of Man Pound'),
        ('GGP', 'Guernsey Pound'),
        ('ZMW', 'Zambian Kwacha'),
    ]

register(NumberCurrencyTransform())
