from collections import namedtuple

UflAttributeDescription = namedtuple('UflAttributeDescription', ('accessor', 'type'))


class UflType:
    ALLOWED_DIRECT_ATTRIBUTES = {}
    
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
    
    def is_convertible_to(self, other):
        return False
    
    def is_equatable_to(self, other):
        return False
    
    def is_comparable_with(self, other):
        return False
    
    def is_valid_value(self, value):
        raise NotImplementedError
    
    def is_default_value(self, value):
        raise NotImplementedError
    
    def resolve_unknown_generic(self, generics_cache):
        return self
    
    def resolve_generic(self, actual_type, generics_cache):
        if self.is_assignable_from(actual_type):
            return actual_type
        return None
    
    def __str__(self):
        return 'Type'
    
    def __repr__(self):
        return '<UflType {0}>'.format(self)
