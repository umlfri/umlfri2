from .type import UflType


class UflAnyType(UflType):
    def is_same_as(self, other):
        return True
    
    @staticmethod
    def parse(value):
        return value
    
    def __str__(self):
        return 'Any'
