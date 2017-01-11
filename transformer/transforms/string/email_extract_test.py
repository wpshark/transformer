# -*- coding: UTF-8 -*-
import unittest
import email_extract


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
            u"email@example.com",
            u"firstname.lastname@example.com",
            u"email@subdomain.example.com",
            u"firstname+lastname@example.com",
            u"email@123.123.123.123",
            u"email@[123.123.123.123]",
            u"\"email\"@example.com",
            u"1234567890@example.com",
            u"email@example-one.com",
            u"_______@example.com",
            u"email@example.name",
            u"email@example.museum",
            u"email@example.co.jp",
            u"firstname-lastname@example.com",
            u"\".firstname\"@example.com",
            u"\"firstname.\"@example.com",
            u"\".firstname.\"@example.com",
            u"\"first..name\"@example.com",
        ]

        possibly_valid_emails = [
            (u"firstname...lastname@example.com", u"lastname@example.com"),
            (u"firstname..lastname@example.com", u"lastname@example.com"),
            (u"firstname..lastname..awesome@example.com", u"awesome@example.com"),
            (u".firstname@example.com", u"firstname@example.com"),
            (u"done. firstname@example.com", u"firstname@example.com")
        ]

        invalid_emails = [
            u"plainaddress",
            u"#@%^%#$@#$@#.com",
            u"@example.com",
            u"email.example.com",
            u"あいうえお@example.com",
            u"email@example",
            u"\"(),:;<>[\]@example.com",
            u"firstname.@example.com",
            u".firstname.@example.com",
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
