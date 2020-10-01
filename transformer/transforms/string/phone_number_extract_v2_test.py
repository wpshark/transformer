import unittest
import phone_number_extract_v2

class TestStringPhoneExtractV2Transform(unittest.TestCase):
    def test_phoneextract(self):
        transformer = phone_number_extract_v2.StringPhoneExtractV2Transform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("This is a test without a phone number"), "")
        self.assertEqual(transformer.transform("my phone number is 123-456-7890"), "123-456-7890")
        self.assertEqual(transformer.transform("bob said to call him at and 321-0989."), "")
        self.assertEqual(transformer.transform("The post office's number is (800) 777-9988 and it costs $53 a month"), "(800) 777-9988")
        self.assertEqual(transformer.transform("Call bob at (+66) 81 23 55 tomorrow at 2 PM"), "(+66) 81 23 55")
