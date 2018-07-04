# -*- coding: utf-8 -*-
import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform

# Regex via http://daringfireball.net/2010/07/improved_regex_for_matching_urls
# Update version via https://gist.github.com/gruber/249502
URL_REGEX = r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""" # NOQA

class StringURLExtractTransform(BaseTransform):

    category = 'string'
    name = 'url_extract'
    label = 'Extract URL'
    help_text = 'Find and copy a web URL out of a text field. Finds the first URL only.'

    noun = 'Text'
    verb = 'find and copy a web URL from'

    def transform(self, str_input, **kwargs):
        if isinstance(str_input, basestring):
            match = re.search(URL_REGEX, str_input)
            return match.group(0) if match else u''
        else:
            return u''


register(StringURLExtractTransform())
