import collections
import re

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
    date

    """
    keys = ['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']

    delta = collections.OrderedDict()
    for key in keys:
        matches = re.findall('((?:-\s*)?\d+)\s?{}?'.format(key), input_)
        if not matches:
            delta[key] = 0
            continue
        for m in matches:
            delta[key] = int(m) if m else 0
    return delta


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
