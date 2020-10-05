import unittest
import phone

#we should do some external validation against https://libphonenumber.appspot.com/

#update on 10/5 - added new tests when validate option is set to True

class TestPhoneNumberFormattingTransform(unittest.TestCase):
    def test_phone(self):
        transformer = phone.PhoneNumberFormattingTransform()

        tests = [
            # input, format, expected output, region
            ('8005551212', '0', '+18005551212', 'US'),
            ('8005551212', '1', '+1 800-555-1212', 'US'),
            ('8005551212', '2', '(800) 555-1212', 'US'),
            ('8005551212', '3', '+1-800-555-1212', 'US'),
            ('8005551212', '4', '800-555-1212', 'US'),
            ('8005551212', '5', '+1 800 555 1212', 'US'),
            ('8005551212', '6', '800 555-1212', 'US'),
            ('8005551212', '7', '8005551212', 'US'),
            ('8005551212', '8', '18005551212', 'US'),

            ('18005551212', '0', '+18005551212', 'US'),
            ('18005551212', '1', '+1 800-555-1212', 'US'),
            ('18005551212', '2', '(800) 555-1212', 'US'),
            ('18005551212', '3', '+1-800-555-1212', 'US'),
            ('18005551212', '4', '800-555-1212', 'US'),
            ('18005551212', '5', '+1 800 555 1212', 'US'),
            ('18005551212', '6', '800 555-1212', 'US'),
            ('18005551212', '7', '8005551212', 'US'),
            ('18005551212', '8', '18005551212', 'US'),

            ('(800) 555-1212', '0', '+18005551212', 'US'),
            ('(800) 555-1212', '1', '+1 800-555-1212', 'US'),
            ('(800) 555-1212', '2', '(800) 555-1212', 'US'),
            ('(800) 555-1212', '3', '+1-800-555-1212', 'US'),
            ('(800) 555-1212', '4', '800-555-1212', 'US'),
            ('(800) 555-1212', '5', '+1 800 555 1212', 'US'),
            ('(800) 555-1212', '6', '800 555-1212', 'US'),
            ('(800) 555-1212', '7', '8005551212', 'US'),
            ('(800) 555-1212', '8', '18005551212', 'US'),

            ('+448005551212', '0', '+448005551212', 'US'),
            ('+448005551212', '1', '+44 800 555 1212', 'US'),
            ('+448005551212', '2', '(0800) 555 1212', 'US'),
            ('+448005551212', '3', '+44-800-555-1212', 'US'),
            ('+448005551212', '4', '800 555 1212', 'US'),
            ('+448005551212', '5', '+44 800 555 1212', 'US'),
            ('+448005551212', '6', '0800 555 1212', 'US'),
            ('+448005551212', '7', '08005551212', 'US'),
            ('+448005551212', '8', '448005551212', 'US'),

            ('+4 48 005 551 212', '0', '+448005551212', 'US'),
            ('+4 48 005 551 212', '1', '+44 800 555 1212', 'US'),
            ('+4 48 005 551 212', '2', '(0800) 555 1212', 'US'),
            ('+4 48 005 551 212', '3', '+44-800-555-1212', 'US'),
            ('+4 48 005 551 212', '4', '800 555 1212', 'US'),
            ('+4 48 005 551 212', '5', '+44 800 555 1212', 'US'),
            ('+4 48 005 551 212', '6', '0800 555 1212', 'US'),
            ('+4 48 005 551 212', '7', '08005551212', 'US'),
            ('+4 48 005 551 212', '8', '448005551212', 'US'),

            ('+44 (800) 5551212', '0', '+448005551212', 'US'),
            ('+44 (800) 5551212', '1', '+44 800 555 1212', 'US'),
            ('+44 (800) 5551212', '2', '(0800) 555 1212', 'US'),
            ('+44 (800) 5551212', '3', '+44-800-555-1212', 'US'),
            ('+44 (800) 5551212', '4', '800 555 1212', 'US'),
            ('+44 (800) 5551212', '5', '+44 800 555 1212', 'US'),
            ('+44 (800) 5551212', '6', '0800 555 1212', 'US'),
            ('+44 (800) 5551212', '7', '08005551212', 'US'),
            ('+44 (800) 5551212', '8', '448005551212', 'US'),

            ('00448005551212', '0', '+448005551212', 'GB'),
            ('00448005551212', '1', '+44 800 555 1212', 'GB'),
            ('00448005551212', '2', '(0800) 555 1212', 'GB'),
            ('00448005551212', '3', '+44-800-555-1212', 'GB'),
            ('00448005551212', '4', '800 555 1212', 'GB'),
            ('00448005551212', '5', '+44 800 555 1212', 'GB'),
            ('00448005551212', '6', '0800 555 1212', 'GB'),
            ('00448005551212', '7', '08005551212', 'GB'),
            ('00448005551212', '8', '448005551212', 'GB'),

            ('0911611611', '0', '+27911611611', 'ZA'),
            ('0911611611', '1', '+27 91 161 1611', 'ZA'),
            ('0911611611', '2', '(091) 161 1611', 'ZA'),
            ('0911611611', '3', '+27-91-161-1611', 'ZA'),
            ('0911611611', '4', '91 161 1611', 'ZA'),
            ('0911611611', '5', '+27 91 161 1611', 'ZA'),
            ('0911611611', '6', '091 161 1611', 'ZA'),
            ('0911611611', '7', '0911611611', 'ZA'),
            ('0911611611', '8', '27911611611', 'ZA'),

            # Custom Value test - Ireleand (IE)
            ('(071) 345 6789', '0', '+353713456789', 'IE'),
            ('(071) 345 6789', '1', '+353 71 345 6789', 'IE'),
            ('(071) 345 6789', '2', '(071) 345 6789', 'IE'),
            ('(071) 345 6789', '3', '+353-71-345-6789', 'IE'),
            ('(071) 345 6789', '4', '71 345 6789', 'IE'),
            ('(071) 345 6789', '5', '+353 71 345 6789', 'IE'),
            ('(071) 345 6789', '6', '071 345 6789', 'IE'),
            ('(071) 345 6789', '7', '0713456789', 'IE'),
            ('(071) 345 6789', '8', '353713456789', 'IE'),
        ]

        for input_number, format_string, expected_output, region in tests:
            self.assertEqual(expected_output, transformer.transform(input_number, format_string=format_string, default_region=region))

    def test_invalid_phone(self):
        transformer = phone.PhoneNumberFormattingTransform()

        tests = [
            # invalid phone numbers
            # input, format, expected output
            ('5551212', '1', '5551212'),
            ('555-1212', '1', '555-1212'),
            ('1555-1212', '1', '555-1212'),
            ('1-22-555-1212', '1', '555-1212'),
        ]

        for input_number, format_string, expected_output in tests:
            out = transformer.transform(input_number, format_string=format_string)
            self.assertEqual(out, input_number)

    def test_invalid_phone_dont_validate(self):
        # set validation to false, we should format these bogus numbers, even if we know they are wrong
        # but still return string if phone number is not entered
        transformer = phone.PhoneNumberFormattingTransform()

        tests = [
            # invalid phone numbers
            # input, format, expected output
            ('(999) 999-9999', '1', False, '+1 999-999-9999'),
            ('1-22-555-1212', '1', False, '+1 1225551212'),
            ('fred', '1', False, 'fred')

        ]

        for input_number, format_string, validate, expected_output in tests:
            self.assertEqual(expected_output, transformer.transform(input_number, format_string=format_string, validate=False))

        

    def test_empty_phone(self):
        transformer = phone.PhoneNumberFormattingTransform()

        out = transformer.transform(None, format_string='1')
        self.assertEqual(out, '')

        out = transformer.transform('', format_string='1')
        self.assertEqual(out, '')

        out = transformer.transform('Something', format_string='1')
        self.assertEqual(out, 'Something')
