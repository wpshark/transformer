import unittest
from . import phone_number_extract

class TestStringPhoneExtractTransform(unittest.TestCase):
    def test_phoneextract(self):
        transformer = phone_number_extract.StringPhoneExtractTransform()

        # using the default regex - which is uni1
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("This is a test without a phone number"), "")
        self.assertEqual(transformer.transform("my phone number is 123-456-7890"), "123-456-7890")
        self.assertEqual(transformer.transform("bob said to call him at and 321-0989."), "321-0989")
        self.assertEqual(transformer.transform("The post office's number is (800) 777-9988 and it costs $53 a month"), "(800) 777-9988")
        self.assertEqual(transformer.transform("Call bob at +66.81.234.5566 tomorrow at 2 PM"), "+66.81.234.5566")

        #using NA 
        tests = [
            # input, format, expected output
            ('this is a NA (999) 999-9999 here', 'na','(999) 999-9999'),
            ('this is not a NA 1-22-555-1212 here', 'na',''),
            ('fred', 'na','')
        ]

        for input_text, regex, expected_output in tests:
            self.assertEqual(expected_output, transformer.transform(input_text, regex=regex))
        
        # using IN
        tests = [
            # input, format, expected output
            ('this is 543-3456 a IN (55)44-33-22-11 here', 'in','(55)44-33-22-11'),
            ('this to IN (55)44*33*22*11 here', 'in','(55)44*33*22*11'),
            ('this is a IN 999-999-9999 here', 'in',''),
            ('fred', 'in','')
        ]

        for input_text, regex, expected_output in tests:
            self.assertEqual(expected_output, transformer.transform(input_text, regex=regex))

        # using UNI2
        tests = [
            # input, format, expected output
            ('this is 543-3456 a IN (55)44-33-22-11 here', 'uni2','543-3456'),
            ('this to IN (55)44*33*22*11 here', 'uni2','(55)44*33*22*11'),
            ('this is a IN 999-999-9999 here', 'uni2','999-999-9999'),
            ('fred', 'uni2','')
        ]

        for input_text, regex, expected_output in tests:
            self.assertEqual(expected_output, transformer.transform(input_text, regex=regex))
