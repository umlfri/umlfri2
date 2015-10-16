from .type import UflType


class UflAnyType(UflType):
    def isSameAs(self, other):
        return True
    
    def __str__(self):
        return 'Any'
