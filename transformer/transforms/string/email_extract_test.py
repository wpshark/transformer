# -*- coding: UTF-8 -*-
import unittest
from . import email_extract


class TestStringEmailExtractTransform(unittest.TestCase):
    def test_emailextract(self):
        transformer = email_extract.StringEmailExtractTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("I do not have email"), "")
        self.assertEqual(transformer.transform("my email is thomas@hils.us"), "thomas@hils.us")
        self.assertEqual(transformer.transform("my email is broken thomas@hils .com"), "")
        self.assertEqual(transformer.transform("my email is broken thomas+hils@gmail.com"), "thomas+hils@gmail.com")

        self.assertEqual(transformer.transform("some quoted \"email@gmail.com\" text"), "email@gmail.com")
        self.assertEqual(transformer.transform("some quoted \\\"email@gmail.com\\\" text"), "email@gmail.com")

        message = "something \"58jv9nv79038tn0@zapzap.com\" on Monday November 28"
        self.assertEqual(transformer.transform(message), "58jv9nv79038tn0@zapzap.com")

        message = "something \"58jv9nv79038tn0@zapzap.com\" on Monday November 28"
        self.assertEqual(transformer.transform(message), "58jv9nv79038tn0@zapzap.com")

        message = "something \"58jv9nv79038tn0@zapzap.com\" on Monday November 28"
        self.assertEqual(transformer.transform(message), "58jv9nv79038tn0@zapzap.com")

    def test_emailvalidation(self):
        valid_emails = [
            "email@example.com",
            "firstname.lastname@example.com",
            "email@subdomain.example.com",
            "firstname+lastname@example.com",
            "email@123.123.123.123",
            "email@[123.123.123.123]",
            "\"email\"@example.com",
            "1234567890@example.com",
            "email@example-one.com",
            "_______@example.com",
            "email@example.name",
            "email@example.museum",
            "email@example.co.jp",
            "firstname-lastname@example.com",
            "\".firstname\"@example.com",
            "\"firstname.\"@example.com",
            "\".firstname.\"@example.com",
            "\"first..name\"@example.com",
        ]

        possibly_valid_emails = [
            ("firstname...lastname@example.com", "lastname@example.com"),
            ("firstname..lastname@example.com", "lastname@example.com"),
            ("firstname..lastname..awesome@example.com", "awesome@example.com"),
            (".firstname@example.com", "firstname@example.com"),
            ("done. firstname@example.com", "firstname@example.com")
        ]

        invalid_emails = [
            "plainaddress",
            "#@%^%#$@#$@#.com",
            "@example.com",
            "email.example.com",
            "あいうえお@example.com",
            "email@example",
            "\"(),:;<>[\]@example.com",
            "firstname.@example.com",
            ".firstname.@example.com",
        ]

        transformer = email_extract.StringEmailExtractTransform()

        for email in valid_emails:
            self.assertEqual(transformer.transform(email), email)
            self.assertEqual(transformer.transform("123--- %s ---456" % email), email)

        for email, expected in possibly_valid_emails:
            self.assertEqual(transformer.transform(email), expected)
            self.assertEqual(transformer.transform("123--- %s ---456" % email), expected)

        for email in invalid_emails:
            self.assertEqual(transformer.transform(email), "")
            self.assertEqual(transformer.transform("123--- %s ---456" % email), "")
