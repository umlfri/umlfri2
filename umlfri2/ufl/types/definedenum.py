from .enum import UflEnumType
from .enumpossibility import UflEnumPossibility


class UflDefinedEnumType(UflEnumType):
    def __init__(self, type, possibilities={}, default=None):
        self.__possibilities = possibilities.copy()
        self.__type = type
        
        super().__init__(tuple(UflEnumPossibility(self, key, value) for key, value in possibilities.items()), default)
    
    @property
    def name(self):
        return self.__type.__name__
    
    @property
    def type(self):
        return self.__type
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.__type == other.__type
    
    def __str__(self):
        return 'DefinedEnum[{0}]'.format(self.name)
