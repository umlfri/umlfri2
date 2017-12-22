from collections import namedtuple

UflMethodDescription = namedtuple('UflMethodDescription', ('selector', 'parameters', 'return_type'))
UflAttributeDescription = namedtuple('UflAttributeDescription', ('accessor', 'type'))

class UflType:
    ALLOWED_DIRECT_ATTRIBUTES = {}
    ALLOWED_DIRECT_METHODS = {}
    
    __parent = None
    
    @property
    def parent(self):
        return self.__parent
    
    def build_default(self, generator):
        raise NotImplementedError
    
    def is_assignable_from(self, other):
        return isinstance(other, self.__class__)
    
    def set_parent(self, parent):
        if self.__parent is not None:
            raise Exception
        self.__parent = parent
    
    @property
    def is_immutable(self):
        raise NotImplementedError
    
    @property
    def is_convertable_to_string(self):
        return False
    
    def is_equatable_to(self, other):
        return False
    
    def is_comparable_with(self, other):
        return False
    
    def is_valid_value(self, value):
        raise NotImplementedError
    
    def is_default_value(self, value):
        raise NotImplementedError
    
    def __str__(self):
        return 'Type'
    
    def __repr__(self):
        return '<UflType {0}>'.format(self)
