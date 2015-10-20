from .type import UflType


class UflAnyType(UflType):
    def is_same_as(self, other):
        return True
    
    def __str__(self):
        return 'Any'
