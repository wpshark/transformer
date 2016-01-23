from transformer.registry import register
from transformer.transforms.base import BaseTransform
from bs4 import BeautifulSoup

class StringStripHtmlTransform(BaseTransform):

    category = 'string'
    name = 'strip html'
    label = 'String / Strip HTML'
    help_text = 'Remove every HTML tag to leave just the plain text.'

    def transform(self, str_input, **kwargs):
        #return re.sub("<.*?>", "", str_input) if str_input else ''
        soup = BeautifulSoup(str_input, 'html.parser')
        return soup.get_text()

register(StringStripHtmlTransform())
