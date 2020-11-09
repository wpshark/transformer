from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number

import random


class UtilChooseTransform(BaseTransform):

    category = 'util'
    name = 'choose'
    label = 'Pick from list'
    help_text = 'Pick the first, last, random, or n-th value that is not empty.'

    noun = 'Values'
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
        if not inputs:
            if options is not None and options.get('default') is not None:
                return options.get('default')
            return ''

        if not isinstance(inputs, list):
            self.raise_exception('Choose requires a list of inputs')

        if options is None:
            options = {}

        default = options.get('default')

        op = options.get('operation', None)
        if op is None or op == '':
            self.raise_exception('Missing Operation')

        if op in self._operations:
            op_func = self._operations[op]
            return op_func(inputs, default=default)

        i = try_parse_number(op, cls=int, default=None)
        if i is None:
            return default

        return self.choose_nth(i, inputs, default=default)


    def all_fields(self, **kwargs):
        return [
            self.build_help_field(),
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


    def truthy_inputs(self, inputs):
        """ return only truthy inputs """
        return [v for v in inputs if (not isinstance(v, str) and v is not None) or v]


    def choose_first(self, inputs, default=None):
        """
        choose the first _truthy_ string value or the first non-string value
        or the default value if there is neither.

        """
        return self.choose_nth(0, inputs, default=default)


    def choose_last(self, inputs, default=None):
        """
        choose the last _truthy_ string value or the last non-string value
        or the default value if there is none.

        """
        return self.choose_nth(-1, inputs, default=default)


    def choose_nth(self, n, inputs, default=None):
        """
        choose the n-th _truthy_ string value or the n-th non-string value
        or the default value if there is neither.

        """
        try:
            return self.truthy_inputs(inputs)[n]
        except:
            pass
        return default


    def choose_random(self, inputs, default=None):
        """
        choose a random _truthy_ string value or a random non-string value
        or the default value if there is neither.

        """
        truthy = self.truthy_inputs(inputs)
        if not truthy:
            return default
        return random.choice(truthy)


register(UtilChooseTransform())
