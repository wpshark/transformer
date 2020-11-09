# -*- coding: utf8 -*-
import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform


class StringEmailExtractTransform(BaseTransform):

    category = 'string'
    name = 'email_extract'
    label = 'Extract Email Address'
    help_text = 'Find and copy an email address out of a text field. Finds the first email address only.'

    noun = 'Text'
    verb = 'find and copy an email address from'

    def transform(self, str_input, **kwargs):
        """
        The local-part of the email address may use any of these ASCII characters:

            Uppercase and lowercase English letters (a–z, A–Z)
            Digits 0 to 9
            Characters ! # $ % & ' * + - / = ? ^ _ ` { | } ~
            Character . provided that it is not the first or last character,
            and provided also that it does not appear two or more times consecutively (e.g. John..Doe@example.com).

            These rules change for quoted strings "as..df"@example.com which allows any
            combination of printable ASCII characters except backslash and doublequote.

        """
        if isinstance(str_input, str):
            match = re.search(r"""
                (
                    "( [a-zA-Z0-9!#$%&'*/=?^_`{|}~+.,)(><-]+ )"
                     |
                     ( (?!\.) ( [a-zA-Z0-9!#$%&'*/=?^_`{|}~+-] | (?<!\.)\. )+ (?<!\.) )
                )
                @
                (
                    (\[?[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\]?)
                    |
                    ([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)
                )
            """, str_input, re.U | re.VERBOSE)
            return match.group(0) if match else ''
        else:
            return ''


register(StringEmailExtractTransform())
