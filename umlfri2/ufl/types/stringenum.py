from .enum import UflEnumType
from .enumpossibility import UflEnumPossibility
from .bool import UflBoolType
from .string import UflStringType


class UflStringEnumType(UflEnumType):
    def __init__(self, possibilities, default=None):
        
        super().__init__((UflEnumPossibility(self, name, name) for name in possibilities), default)
    
    def is_assignable_from(self, other):
        if not isinstance(other, UflStringEnumType):
            return False
        
        return all(x.name == y.name for x, y in zip(self.possibilities, other.possibilities))

    def is_convertible_to(self, other):
        return isinstance(other, UflStringType)
    
    def is_equatable_to(self, other):
        from .string import UflStringType
        if isinstance(other, UflStringType):
            return True
        
        if not isinstance(other, UflStringEnumType):
            return False
        
        return self.possibilities == other.possibilities
    
    def __str__(self):
        return 'Enum[{0}]'.format(", ".join(possibility.name for possibility in self.possibilities))
