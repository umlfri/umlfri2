from .type import UflType


class UflNullableType(UflType):
    def __init__(self, inner_type):
        self.__inner_type = inner_type
    
    @property
    def inner_type(self):
        return self.__inner_type
    
    def build_default(self):
        return None
    
    def parse(self, value):
        return self.__inner_type.parse(value)
    
    def isSameAs(self, other):
        if other is None:
            return True
        
        if not super().isSameAs(other):
            return False
        
        if self.__inner_type.isSameAs(other.__inner_type):
            return True
        
        if self.__inner_type.isSameAs(other):
            return True
        
        return False
    
    def __str__(self):
        return "Nullable[{0}]".format(self.__inner_type)
