# ~*~ coding: utf-8 ~*~
import unittest
from . import url_encode

class TestStringURLEncodeTransform(unittest.TestCase):
    def test_encode(self):
        transformer = url_encode.StringURLEncodeTransform()

        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform(" "), "%20")
        self.assertEqual(transformer.transform(" ", use_plus=True), "+")
        self.assertEqual(transformer.transform("@"), "%40")
        self.assertEqual(transformer.transform("+"), "%2B")
        self.assertEqual(transformer.transform("user+test@example.com"), "user%2Btest%40example.com")
        self.assertEqual(transformer.transform("True != False"), "True%20%21%3D%20False")
        self.assertEqual(transformer.transform("True != False", use_plus=True), "True+%21%3D+False")
        self.assertEqual(transformer.transform("http://www.example.com/+/"), "http%3A//www.example.com/%2B/")
        self.assertEqual(
            transformer.transform("http://www.example.com/+/", use_plus=True), "http%3A%2F%2Fwww.example.com%2F%2B%2F")
        self.assertEqual(transformer.transform("1234567 !@#$%^&*"), "1234567%20%21%40%23%24%25%5E%26%2A")
        self.assertEqual(transformer.transform("1234567 !@#$%^&*", use_plus=True), "1234567+%21%40%23%24%25%5E%26%2A")
        self.assertEqual(transformer.transform("é", use_plus=True), "%C3%A9")
        self.assertEqual(transformer.transform("é", use_plus=False), "%C3%A9")
        self.assertEqual(transformer.transform(b"\xc3\xa9", use_plus=True), "%C3%A9")
        self.assertEqual(transformer.transform(b"\xc3\xa9", use_plus=False), "%C3%A9")
        self.assertEqual(transformer.transform("é", use_plus=False), "%C3%A9")
