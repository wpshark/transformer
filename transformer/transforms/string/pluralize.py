from transformer.registry import register
from transformer.transforms.base import BaseTransform
import inflect

pluralizer = inflect.engine()

class StringPluralizeTransform(BaseTransform):

    category = 'string'
    name = 'pluralize'
    label = 'Pluralize'
    help_text = 'Pluralize any English word (frog turns into frogs; child turns into children)'

    noun = 'Text'
    verb = 'make plural'

    def transform(self, str_input, **kwargs):
        return pluralizer.plural(str_input) if str_input else u''

register(StringPluralizeTransform())
