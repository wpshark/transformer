import unittest
import url_decode

class TestStringURLDecodeTransform(unittest.TestCase):
    def test_decode(self):
        transformer = url_decode.StringURLDecodeTransform()

        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("%20"), " ")
        self.assertEqual(transformer.transform("+", use_plus=True), " ")
        self.assertEqual(transformer.transform("%40"), "@")
        self.assertEqual(transformer.transform("%2B"), "+")
        self.assertEqual(transformer.transform(u"user%2Btest%40example.com"), "user+test@example.com")
        self.assertEqual(transformer.transform("True%20%21%3D%20False"), "True != False")
        self.assertEqual(transformer.transform("True+%21%3D+False", use_plus=True), "True != False")
        self.assertEqual(transformer.transform("http%3A//www.example.com/%2B/"), "http://www.example.com/+/")
        self.assertEqual(transformer.transform("http%3A%2F%2Fwww.example.com%2F%2B%2F", use_plus=True), "http://www.example.com/+/")
        self.assertEqual(transformer.transform("1234567%20%21%40%23%24%25%5E%26%2A"), "1234567 !@#$%^&*")
        self.assertEqual(transformer.transform("1234567+%21%40%23%24%25%5E%26%2A", use_plus=True), "1234567 !@#$%^&*")
