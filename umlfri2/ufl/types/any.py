from .type import UflType


class UflAnyType(UflType):
    def is_assignable_from(self, other):
        return True
    
    def __str__(self):
        return 'Any'
