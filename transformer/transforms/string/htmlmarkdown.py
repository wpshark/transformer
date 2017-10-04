import bs4
import html2text

from transformer.registry import register
from transformer.transforms.base import BaseTransform


class StringHTMLMarkdownTransform(BaseTransform):

    category = 'string'
    name = 'htmlmarkdown'
    label = 'Convert HTML to Markdown'
    help_text = 'Convert valid HTML to Markdown text'

    noun = 'HTML'
    verb = 'convert to Markdown'

    def transform(self, str_input, **kwargs):
        if not str_input:
            return u''

        markdown = html2text.html2text(self.to_unicode_or_bust(str_input))
        markdown = markdown.strip('\n')
        return markdown

    def to_unicode_or_bust(self, obj, encoding='utf-8'):
        try:
            if isinstance(obj, basestring):
                if not isinstance(obj, unicode):
                    obj = unicode(obj, encoding)
            return obj
        except:
            return bs4.UnicodeDammit(obj, is_html=False).unicode_markup

register(StringHTMLMarkdownTransform())
