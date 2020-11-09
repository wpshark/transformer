import html2text

from transformer.util import to_unicode_or_bust
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
            return ''

        markdown = html2text.html2text(to_unicode_or_bust(str_input))
        markdown = markdown.strip('\n')
        return markdown

register(StringHTMLMarkdownTransform())
