from collections import namedtuple

UflMethodDescription = namedtuple('UflMethodDescription', ('selector', 'parameters', 'return_type'))

class UflType:
    ALLOWED_DIRECT_ATTRIBUTES = {}
    ALLOWED_DIRECT_METHODS = {}
    
    def build_default(self):
        raise NotImplementedError
    
    def isSameAs(self, other):
        
        if isinstance(other, self.__class__):
            return True
        
        from .any import UflAnyType
        if isinstance(other, UflAnyType):
            return True
        
        from .nullable import UflNullableType
        if isinstance(other, UflNullableType) and other.inner_type.isSameAs(self):
            return True
        
        return False
    
    def __str__(self):
        return 'Type'
    
    def __repr__(self):
        return '<UflType {0}>'.format(self)
