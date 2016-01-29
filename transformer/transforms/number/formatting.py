from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import APIError

class NumberFormattingTransform(BaseTransform):

    category = 'number'
    name = 'formatting'
    label = 'Format'
    help_text = 'Format a number to a new style. Does not perform any rounding or padding of the number.'

    def transform(self, val, input_decimal_mark, output_format, **kwargs):
        if val is None:
            return u''

        if isinstance(output_format, int):
            output_format = unicode(output_format)

        parts = val.rsplit(input_decimal_mark, 1)
        before_decimal = parts[0]
        after_decimal = parts[1] if len(parts) == 2 else u''

        before_decimal = u''.join([x for x in before_decimal if x in u'1234567890-'])

        # Python will only do comma-grouped numbers, so convert to that by default then modify if needed
        before_decimal = u'{:,}'.format(int(before_decimal))

        if output_format == u'0':
            decimal_mark = u'.'
        elif output_format == u'1':
            before_decimal = before_decimal.replace(u',', u'.')
            decimal_mark = u','
        elif output_format == u'2':
            before_decimal = before_decimal.replace(u',', u' ')
            decimal_mark = u'.'
        elif output_format == u'3':
            decimal_mark = u','
            before_decimal = before_decimal.replace(u',', u' ')
        else:
            raise APIError(u'Format {} not supported'.format(output_format))

        if after_decimal:
            return before_decimal + decimal_mark + after_decimal
        else:
            return before_decimal

    def fields(self, *args, **kwargs):
        available_formats = [
            '0|Comma as grouping & dot as decimal, \
            1|Dot as grouping & comma as decimal, \
            2|Space as grouping & dot as decimal, \
            3|Space as grouping & comma as decimal'
        ]

        return [
            {
                'key': 'input_decimal_mark',
                'type': 'unicode',
                'label': 'Input Decimal Mark',
                'required': True,
                'choices': ['Comma (,)', 'Dot (.)'],
            },
            {
                'key': 'output_format',
                'type': 'unicode',
                'label': 'Desired Format',
                'required': True,
                'choices': available_formats,
            }
        ]


register(NumberFormattingTransform())
