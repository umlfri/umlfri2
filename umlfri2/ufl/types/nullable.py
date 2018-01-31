from .type import UflType
from .bool import UflBoolType
from .string import UflStringType


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
        
        return isinstance(other, UflBoolType)
    
    def __str__(self):
        return "Nullable[{0}]".format(self.__inner_type)
