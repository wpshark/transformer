from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import APIError

class NumberFormattingTransform(BaseTransform):

    category = 'number'
    name = 'formatting'
    label = 'Format Number'
    help_text = 'Format a number to a new style. Does not perform any rounding or padding of the number.'

    noun = 'Number'
    verb = 'format'

    def transform(self, val, input_decimal_mark, output_format, **kwargs):
        if val is None:
            return ''

        if isinstance(output_format, int):
            output_format = str(output_format)

        parts = val.rsplit(input_decimal_mark, 1)
        before_decimal = parts[0]
        after_decimal = parts[1] if len(parts) == 2 else ''

        before_decimal = ''.join([x for x in before_decimal if x in '1234567890-'])

        # Python will only do comma-grouped numbers, so convert to that by default then modify if needed
        try:
            before_decimal = '{:,}'.format(int(before_decimal))
        except ValueError:
            # Return original input if we can't do anything with it
            return val

        if output_format == '0':
            decimal_mark = '.'
        elif output_format == '1':
            before_decimal = before_decimal.replace(',', '.')
            decimal_mark = ','
        elif output_format == '2':
            before_decimal = before_decimal.replace(',', ' ')
            decimal_mark = '.'
        elif output_format == '3':
            decimal_mark = ','
            before_decimal = before_decimal.replace(',', ' ')
        else:
            raise APIError('Format {} not supported'.format(output_format))

        if after_decimal:
            return before_decimal + decimal_mark + after_decimal
        else:
            return before_decimal

    def fields(self, *args, **kwargs):
        available_formats = {
            '0': 'Comma for grouping & period for decimal',
            '1': 'Period for grouping & comma for decimal',
            '2': 'Space for grouping & period for decimal',
            '3': 'Space for grouping & comma for decimal'
        }

        return [
            {
                'key': 'input_decimal_mark',
                'type': 'unicode',
                'label': 'Input Decimal Mark',
                'help_text': 'The character the input uses to denote the decimal/fractional portion of the number.',
                'required': True,
                'choices': {'.': 'Period', ',': 'Comma'},
            },
            {
                'key': 'output_format',
                'type': 'unicode',
                'label': 'To Format',
                'help_text': 'The format the number will be converted to.',
                'required': True,
                'choices': available_formats,
            }
        ]


register(NumberFormattingTransform())
