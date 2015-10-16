from collections import namedtuple

UflMethodDescription = namedtuple('UflMethodDescription', ('selector', 'parameters', 'return_type'))

class UflType:
    ALLOWED_DIRECT_ATTRIBUTES = {}
    ALLOWED_DIRECT_METHODS = {}
    
    def build_default(self):
        raise NotImplementedError
    
    def __str__(self):
        return 'Type'
    
    def __repr__(self):
        return '<UflType {0}>'.format(self)
