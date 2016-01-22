import json

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


def smart_dump(v):
    """
    if the value is a string, just return it because that's ok to display...
    otherwise, json dumps it!

    """
    if isinstance(v, basestring) or isinstance(v, str):
        return v
    else:
        return json.dumps(v)
