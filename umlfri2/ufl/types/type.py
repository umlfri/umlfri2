from collections import namedtuple

UflMethodDescription = namedtuple('UflMethodDescription', ('selector', 'parameters', 'return_type'))

class UflType:
    ALLOWED_DIRECT_ATTRIBUTES = {}
    ALLOWED_DIRECT_METHODS = {}
