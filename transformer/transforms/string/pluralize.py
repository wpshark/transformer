from transformer.registry import register
from transformer.transforms.base import BaseTransform
import inflect
p = inflect.engine()

class StringPluralizeTransform(BaseTransform):

    category = 'string'
    name = 'pluralize'
    label = 'String / Pluralize'
    help_text = 'Pluralize any English word (frog turns into frogs; child turns into children)'

    def transform(self, str_input, **kwargs):
        return p.plural(str_input) if str_input else ''

register(StringPluralizeTransform())