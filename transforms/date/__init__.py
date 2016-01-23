import util
__all__ = util.import_submodules(__name__).keys()

import arrow
import datetime
import dateutil.parser

def try_parse(date_value, from_format=None):
    """
    try to parse a int or string value into a datetime format

    """
    try:
        # check to see if the string can be converted into a float (a timestamp)
        try:
            date_value = float(date_value)
        except:
            pass

        # if this is a unix string... or a milliseconds since epoch
        if isinstance(date_value, int) or isinstance(date_value, long) or isinstance(date_value, float):
            if date_value >= (1 << 32) - 1:
                date_value /= 1000.0
            return datetime.datetime.fromtimestamp(date_value)

        # otherwise, try to parse the date value from the from_format
        if from_format:
            dt = arrow.get(date_value, from_format)
            if dt:
                return dt
    except:
        pass

    # otherwise, use the fuzzy parser
    return dateutil.parser.parse(date_value, fuzzy=True)
