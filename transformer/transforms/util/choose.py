from transformer.registry import register
from transformer.transforms.base import BaseTransform

import random


class UtilChooseTransform(BaseTransform):

    category = 'util'
    name = 'choose'
    label = 'Pick from list'
    help_text = 'Pick the first, last, or random value that is not empty.'

    noun = 'Value'
    noun_plural = 'Values'
    verb = 'choose from'

    def __init__(self):
        self._operations = {
            'first': self.choose_first,
            'last': self.choose_last,
            'random': self.choose_random
        }

    def transform_many(self, inputs, options=None, **kwargs):
        """
        Override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform the choose operation.

        """
        if not isinstance(inputs, list):
            self.raise_exception('Choose requires a list of inputs')

        if options is None:
            options = {}

        op = options.get('operation')
        if not op or op not in self._operations:
            self.raise_exception('Invalid Operation')

        default = options.get('default')

        op_func = self._operations[op]

        return op_func(inputs, default=default)


    def all_fields(self, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'operation',
                'choices': 'first|Choose First,last|Choose Last,random|Choose Random',
                'help_text': 'Value to choose.'
            },
            self.build_list_input_field(),
            {
                'type': 'unicode',
                'required': False,
                'key': 'default',
                'help_text': 'Optional default value to use if no item could be choosen.'
            },
        ]


    def choose_first(self, inputs, default=None):
        """
        choose the first _truthy_ string value or the first non-string value
        or the default value if there is neither.

        """
        first = default
        for v in inputs:
            # if this value is a string and is falsy (i.e., empty) skip it
            if isinstance(v, basestring) and not v:
                continue
            # otherwise, we have a valid first value...use it
            first = v
            break
        return first


    def choose_last(self, inputs, default=None):
        """
        choose the last _truthy_ string value or the last non-string value
        or the default value if there is none.

        """
        return self.choose_first(reversed(inputs), default=default)


    def choose_random(self, inputs, default=None):
        """
        choose a random _truthy_ string value or a random non-string value
        or the default value if there is neither.

        """
        truthy = [v for v in inputs if not isinstance(v, basestring) or v]
        if not truthy:
            return default
        return random.choice(truthy)


register(UtilChooseTransform())
