import unittest
import url_extract

class TestStringURLExtractTransform(unittest.TestCase):
    def test_urlextract(self):
        transformer = url_extract.StringURLExtractTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("I do not have a website"), "")
        self.assertEqual(transformer.transform("my site is google.com"), "google.com")
        self.assertEqual(transformer.transform("some www.google.com web address www.yahoo.com"), "www.google.com")
        self.assertEqual(transformer.transform("some http://www.google.com web address www.yahoo.com"), "http://www.google.com")
        self.assertEqual(transformer.transform("some <a href='http://www.google.com'>test</a> web address www.yahoo.com"), "http://www.google.com")
