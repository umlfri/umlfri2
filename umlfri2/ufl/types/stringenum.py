from .enum import UflEnumType, UflEnumPossibility


class UflStringEnumType(UflEnumType):
    def __init__(self, possibilities, default=None):
        
        super().__init__((UflEnumPossibility(self, name, name) for name in possibilities), default)
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.possibilities == other.possibilities
    
    def __str__(self):
        return 'Enum[{0}]'.format(", ".join(self.__possibilities))
