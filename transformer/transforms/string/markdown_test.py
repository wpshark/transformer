# -*- coding: utf-8 -*-
import unittest
import markdowntohtml

class TestMarkdownHTMLTransform(unittest.TestCase):
    def test_markdowntohtml(self):
        transformer = markdowntohtml.StringMarkdownHTMLTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("* thing"), "<ul>\n<li>thing</li>\n</ul>")
        self.assertEqual(transformer.transform('![image](http://zapier.com/image.png)'), '<p><img alt="image" src="http://zapier.com/image.png" /></p>')
        self.assertEqual(transformer.transform("# Header"), "<h1>Header</h1>")
        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("[link](http://google.com)"), '<p><a href="http://google.com">link</a></p>')

    def test_markdowntohtml_unicode(self):
        transformer = markdowntohtml.StringMarkdownHTMLTransform()
        self.assertEqual(transformer.transform(u""), u"")
        self.assertEqual(transformer.transform(u"* thing"), u"<ul>\n<li>thing</li>\n</ul>")
        self.assertEqual(transformer.transform(u"* \u5b57 thing"), u"<ul>\n<li>\u5b57 thing</li>\n</ul>")
        self.assertEqual(transformer.transform(u"\ufeff\u062a\u0627\u0632\u06c1"), u"<p>\ufeff\u062a\u0627\u0632\u06c1</p>")
        self.assertEqual(transformer.transform("\xef\xbb\xbf\xd8\xaa\xd8\xa7\xd8\xb2\xdb\x81"), u"<p>\ufeff\u062a\u0627\u0632\u06c1</p>")
