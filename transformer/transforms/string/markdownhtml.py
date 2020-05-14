import markdown

from transformer.util import to_unicode_or_bust
from transformer.registry import register
from transformer.transforms.base import BaseTransform


class StringMarkdownHTMLTransform(BaseTransform):

    category = 'string'
    name = 'markdown'
    label = 'Convert Markdown to HTML'
    help_text = 'Convert Markdown text into valid HTML'

    noun = 'Markdown text'
    verb = 'convert to HTML'

    def transform(self, str_input, **kwargs):
        return markdown.markdown(to_unicode_or_bust(str_input)) if str_input else u''

register(StringMarkdownHTMLTransform())
