from .type import UflType


class UflAnyType(UflType):
    def is_assignable_from(self, other):
        return True
    
    @staticmethod
    def parse(value):
        return value
    
    def __str__(self):
        return 'Any'
