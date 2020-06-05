import pdb
import arrow
import dateutil.parser
import pytz
import parsedatetime

import collections
import datetime
import re
from decimal import Decimal

RELATIVE_KEYWORDS = ('next', 'last', 'yesterday', 'tomorrow', 'from', 'before')

class APIError(Exception):
    """ Base Exception for the API """
    status_code = 400

    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = self.status_code
        return rv


def tdelta(input_):
    """
    convert a human readable time delta into a dictionary that can be used
    to create an actual time delta object or other method for manipulating a
    date.

    * positive and negative values are allowed
    * multiple values of the same key are summed together

    >>> tdelta('5 months 4 weeks 3 days -1mo').get('months')
    4

    >>> tdelta('+ 1day - 5 days').get('days')
    -4

    """
    matcher = re.compile(r"""(?:
        (?P<years>    ((?:[-+]\s*)?\d+))\s*y((ea)?r(s)?)?   | # y, yr, yrs, year, years
        (?P<months>   ((?:[-+]\s*)?\d+))\s*mo(nth(s)?)?     | # mo, month, months
        (?P<weeks>    ((?:[-+]\s*)?\d+))\s*w((ee)?(k(s)?)?) | # w, wk, wks, week, weeks
        (?P<days>     ((?:[-+]\s*)?\d+))\s*d(ay(s)?)?       | # d, day, days
        (?P<hours>    ((?:[-+]\s*)?\d+))\s*h(ou)?(r(s)?)?   | # h, hr, hrs, hour, hours
        (?P<minutes>  ((?:[-+]\s*)?\d+))\s*m(in(ute)?(s)?)? | # m, min, mins, minute, minutes
        (?P<seconds>  ((?:[-+]\s*)?\d+))\s*s(ec(ond)?(s)?)?   # s, sec, secs, second, seconds
    ) (?:\s|$)
    """, re.U | re.X)

    keys = ['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']

    delta = collections.OrderedDict((k, 0) for k in keys)

    for match in matcher.finditer(input_):
        if not match:
            continue
        for key in keys:
            m = match.group(key)
            if m is None:
                continue
            delta[key] += int(m) if m else 0

    return delta


def shift_date(dt, delta):
    """
    shift a datetime object by the delta amount generated from `tdelta`

    we use dateutil.relativedelta for years, months, weeks and days
    we use datetime.timedelta for hours, minutes, and seconds

    """
    from dateutil.relativedelta import relativedelta
    from datetime import timedelta

    relative_large = {k: v for k, v in delta.items() if k not in ('hours', 'minutes', 'seconds')}
    relative_small = {k: v for k, v in delta.items() if k in ('hours', 'minutes', 'seconds')}

    dt = dt + relativedelta(**relative_large)
    dt = dt + timedelta(**relative_small)
    return dt


def try_parse_date(date_value, from_format=None):
    """
    try to parse a int or string value into a datetime format

    """

    try:
        if from_format:
            dt = arrow.get(date_value, from_format)
            if dt:
                return dt

        try:
            # Assume that a sufficiently large timestamp is actually in millisecond resolution, but with the decimal point missing
            date_value = float(date_value)
            if date_value >= (1 << 32) - 1:
                date_value /= 1000.0
        except:
            pass

        # try parsedatetime first if any of the relative keywords appear
        if isinstance(date_value, basestring) and any(k in date_value for k in RELATIVE_KEYWORDS):
            cal = parsedatetime.Calendar()
            dt, _ = cal.parseDT(datetimeString=date_value, sourceTime=datetime.datetime.now(), tzinfo=pytz.timezone('UTC'))
            if dt:
                return dt

        # try using arrow
        def datetime_to_float(d):
            epoch = datetime.datetime.utcfromtimestamp(0)
            total_seconds =  (d - epoch).total_seconds()
            # total_seconds will be in decimals (millisecond precision)
            return total_seconds

        try:
            pdb.set_trace()
            dtm = datetime.datetime.strptime(date_value, "%d/%m/%Y")
            unchanged = date_value
            return unchanged
        except:
            pass
        #dtm = datetime_to_float(date_value)
        pdb.set_trace()
        dt = arrow.get(date_value)
        if dt:
            return dt
    except:
        pass

    # otherwise, use the fuzzy dateutil parser
    try:
        return dateutil.parser.parse(date_value, fuzzy=True)
    except:
        # `dateutil.parser.parse` raises an exception on certain input, but returns "today" on other inputs
        # so we instead just return a datetime object representing "today" on those exceptions.
        return datetime.datetime(*datetime.datetime.utcnow().utctimetuple()[:3])


def int_or_float(v):
    """
    returns an int if the value is a long or int or a float that can be
    represented by an int...otherwise returns a float
    """
    if isinstance(v, int) or isinstance(v, long):
        return v
    if v.is_integer():
        return long(v)
    return float(v)



def try_parse_number(number_value, cls=float, default=0):
    """
    rudimentary number parsing.
    """
    if isinstance(number_value, int) or isinstance(number_value, long) or isinstance(number_value, float):
        return number_value
    try:
        return int_or_float(cls(number_value))
    except:
        if default is None:
            return default
        return cls(default)


def expand_special_chargroups(str_input):
    """
    helper to replace special character groups with their counterparts

    """
    if not isinstance(str_input, basestring):
        return str_input

    groups = [
        ('[:space:]', ' '),
        ('[:s:]', ' '),
        ('[:tab:]', '\t'),
        ('[:t:]', '\t'),
        ('[:newline:]', '\n'),
        ('[:n:]', '\n'),
        ('[:return:]', '\r'),
        ('[:r:]', '\r'),
    ]

    out = str_input
    for key, value in groups:
        out = out.replace(key, value)
    return out


def import_submodules(package_name):
    """ Import all submodules of a module, recursively

    :param package_name: Package name
    :type package_name: str
    :rtype: dict[types.ModuleType]
    """
    import importlib
    import pkgutil
    import sys
    package = sys.modules[package_name]
    return {
        name: importlib.import_module(package_name + '.' + name)
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }
