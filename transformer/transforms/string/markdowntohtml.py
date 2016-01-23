import markdown
from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringMarkdownHTMLTransform(BaseTransform):

    category = 'string'
    name = 'Markdown'
    label = 'String / Convert Markdown'
    help_text = 'Convert Markdown text into valid HTML'
    

    def transform(self, str_input, **kwargs):
       	return markdown.markdown(str_input) if str_input else ''


register(StringMarkdownHTMLTransform())


