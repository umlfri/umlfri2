from .enum import UflEnumType
from .enumpossibility import UflEnumPossibility


class UflTypedEnumType(UflEnumType):
    def __init__(self, type, default=None):
        self.__type = type
        super().__init__((UflEnumPossibility(self, name, value) for name, value in type.__members__.items()), default)
    
    @property
    def name(self):
        return self.__type.__name__
    
    @property
    def type(self):
        return self.__type
    
    def is_assignable_from(self, other):
        if not isinstance(other, UflTypedEnumType):
            return False
        
        return self.__type == other.__type
    
    def is_equatable_to(self, other):
        if not isinstance(other, UflTypedEnumType):
            return False
        
        return self.__type == other.__type
    
    def __str__(self):
        return 'TypedEnum[{0}]'.format(self.name)
