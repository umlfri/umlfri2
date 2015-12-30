from .type import UflType


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
    
    def is_same_as(self, other):
        if other is None:
            return True
        
        if not super().is_same_as(other):
            return self.__inner_type.is_same_as(other)
        
        if self.__inner_type.is_same_as(other.__inner_type):
            return True
        
        return False
    
    def __str__(self):
        return "Nullable[{0}]".format(self.__inner_type)
