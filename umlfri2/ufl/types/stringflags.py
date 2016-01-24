from .enumpossibility import UflEnumPossibility
from .flags import UflFlagsType


class UflStringFlagsType(UflFlagsType):
    def __init__(self, possibilities, default=None):
        
        super().__init__((UflEnumPossibility(self, name, name) for name in possibilities), default)
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.possibilities == other.possibilities
    
    def __str__(self):
        return 'Flags[{0}]'.format(", ".join(self.__possibilities))
