import unittest
import markdowntohtml

class TestMarkdownHTMLTransform(unittest.TestCase):
    def test_markdowntohtml(self):
        transformer = markdowntohtml.StringMarkdownHTMLTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("* thing"), "<ul>\n<li>thing</li>\n</ul>")
        self.assertEqual(transformer.transform('![image](http://zapier.com/image.png)'), '<img src="http://zapier.com/image.png" alt="image">')
        self.assertEqual(transformer.transform("# Header"), "<h1>Header</h1>")
        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("[link](http://google.com)"), '<a href="http://google.com">link</a>')
