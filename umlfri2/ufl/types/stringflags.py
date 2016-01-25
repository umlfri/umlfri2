from .enumpossibility import UflEnumPossibility
from .flags import UflFlagsType
from .string import UflStringType


class UflStringFlagsType(UflFlagsType):
    def __init__(self, possibilities, default=None):
        super().__init__((UflEnumPossibility(self, name, name) for name in possibilities), default)

    @property
    def item_type(self):
        return UflStringType()
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.possibilities == other.possibilities
    
    def __str__(self):
        return 'Flags[{0}]'.format(", ".join(possibility.name for possibility in self.possibilities))
