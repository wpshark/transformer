from transformer.registry import register
from transformer.transforms.base import BaseTransform
from bs4 import BeautifulSoup

class StringStripHtmlTransform(BaseTransform):

    category = 'string'
    name = 'strip_html'
    label = 'Remove HTML Tags'
    help_text = 'Remove every HTML tag to leave just the plain text.'

    noun = 'HTML'
    verb = 'convert to plain text'

    def transform(self, str_input, **kwargs):
        if not str_input:
            return ''

        soup = BeautifulSoup(str_input, 'html.parser')

        for elem in soup.findAll(['script', 'style']):
            elem.extract()

        return soup.get_text()

register(StringStripHtmlTransform())
