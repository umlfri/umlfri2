from ..base.type import UflType
from ..basic.string import UflStringType


class UflNullableType(UflType):
    def __init__(self, inner_type):
        self.__inner_type = inner_type
    
    @property
    def inner_type(self):
        return self.__inner_type
    
    def build_default(self, generator):
        return None
    
    def parse(self, value):
        return self.__inner_type.parse(value)
    
    def is_assignable_from(self, other):
        if isinstance(other, UflNullableType):
            if other.__inner_type is None:
                return True
            else:
                return self.__inner_type.is_assignable_from(other.__inner_type)
        else:
            return self.__inner_type.is_assignable_from(other)
    
    def is_equatable_to(self, other):
        if isinstance(other, UflNullableType):
            return self.__inner_type.is_equatable_to(other.__inner_type)
        else:
            return self.__inner_type.is_equatable_to(other)
    
    def is_convertible_to(self, other):
        if isinstance(other, UflStringType):
            return self.__inner_type.is_convertible_to(other)
        
        return False
    
    @property
    def is_immutable(self):
        return self.__inner_type.is_immutable

    def is_valid_value(self, value):
        if value is None:
            return True
        return self.__inner_type.is_valid_value(value)
    
    def set_parent(self, parent):
        super().set_parent(parent)
        self.__inner_type.set_parent(self)
    
    def resolve_unknown_generic(self, generics_cache):
        resolved_inner_type = self.__inner_type.resolve_unknown_generic(generics_cache)
        if resolved_inner_type is None:
            return None
        
        return UflNullableType(resolved_inner_type)
    
    def resolve_generic(self, actual_type, generics_cache):
        if not isinstance(actual_type, UflNullableType):
            return None
        
        resolved_inner_type = self.__inner_type.resolve_generic(actual_type.__inner_type, generics_cache)
        if resolved_inner_type is None:
            return None
        
        return UflNullableType(resolved_inner_type)
    
    def __str__(self):
        return "Nullable[{0}]".format(self.__inner_type)
