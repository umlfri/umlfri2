from collections import namedtuple

UflMethodDescription = namedtuple('UflMethodDescription', ('selector', 'parameters', 'return_type'))

class UflType:
    ALLOWED_DIRECT_ATTRIBUTES = {}
    ALLOWED_DIRECT_METHODS = {}
    
    def build_default(self, generator):
        raise NotImplementedError
    
    def is_same_as(self, other):
        if isinstance(other, self.__class__):
            return True
        
        from .any import UflAnyType
        if isinstance(other, UflAnyType):
            return True
        
        from .nullable import UflNullableType
        if isinstance(other, UflNullableType) and other.inner_type.is_same_as(self):
            return True
        
        return False
    
    @property
    def is_immutable(self):
        raise NotImplementedError
    
    def is_valid_value(self, value):
        raise NotImplementedError
    
    def is_default_value(self, value):
        raise NotImplementedError
    
    def __str__(self):
        return 'Type'
    
    def __repr__(self):
        return '<UflType {0}>'.format(self)
