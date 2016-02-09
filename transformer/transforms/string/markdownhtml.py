import bs4
import markdown

from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringMarkdownHTMLTransform(BaseTransform):

    category = 'string'
    name = 'markdown'
    label = 'Convert Markdown to HTML'
    help_text = 'Convert Markdown text into valid HTML'

    noun = 'Markdown text'
    noun_plural = 'Markdown text'
    verb = 'convert to HTML'


    def transform(self, str_input, **kwargs):
        return markdown.markdown(self.to_unicode_or_bust(str_input)) if str_input else u''

    def to_unicode_or_bust(self, obj, encoding='utf-8'):
        try:
            if isinstance(obj, basestring):
                if not isinstance(obj, unicode):
                    obj = unicode(obj, encoding)
            return obj
        except:
            return bs4.UnicodeDammit(obj, is_html=False).unicode_markup

register(StringMarkdownHTMLTransform())
