from collections import namedtuple

UflMethodDescription = namedtuple('UflMethodDescription', ('selector', 'parameters', 'return_type'))

class UflType:
    ALLOWED_DIRECT_ATTRIBUTES = {}
    ALLOWED_DIRECT_METHODS = {}
    
    __parent = None
    
    @property
    def parent(self):
        return self.__parent
    
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
    
    def is_valid_value(self, value):
        raise NotImplementedError
    
    def is_default_value(self, value):
        raise NotImplementedError
    
    def __str__(self):
        return 'Type'
    
    def __repr__(self):
        return '<UflType {0}>'.format(self)
