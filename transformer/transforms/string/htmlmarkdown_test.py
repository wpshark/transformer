# -*- coding: utf-8 -*-
import unittest
import htmlmarkdown


class TestMarkdownHTMLTransform(unittest.TestCase):
    def test_markdowntohtml(self):
        tests = [
            # html, expected markdown
            (None, ''),
            ('', ''),
            ('<ul>\n<li>thing</li>\n</ul>', '  * thing'),
            ('<p><img alt="image" src="http://zapier.com/image.png" /></p>', '![image](http://zapier.com/image.png)'),
            ('<h1>Header</h1>', '# Header'),
            ('<p><a href="http://google.com">link</a></p>', '[link](http://google.com)'),
        ]

        transformer = htmlmarkdown.StringHTMLMarkdownTransform()
        for html, markdown in tests:
            self.assertEqual(transformer.transform(html), markdown)

    def test_markdowntohtml_unicode(self):
        tests = [
            # html, expected markdown
            (None, u''),
            (u'', u''),
            (u'<ul>\n<li>thing</li>\n</ul>', u'  * thing'),
            (u'<ul>\n<li>\u5b57 thing</li>\n</ul>', u'  * \u5b57 thing'),
            (u'<p>\ufeff\u062a\u0627\u0632\u06c1</p>', u'\ufeff\u062a\u0627\u0632\u06c1'),
            (u'<p>\ufeff\u062a\u0627\u0632\u06c1</p>', '\xef\xbb\xbf\xd8\xaa\xd8\xa7\xd8\xb2\xdb\x81'.decode('utf-8')),
        ]
        transformer = htmlmarkdown.StringHTMLMarkdownTransform()
        for html, markdown in tests:
            self.assertEqual(transformer.transform(html), markdown)
