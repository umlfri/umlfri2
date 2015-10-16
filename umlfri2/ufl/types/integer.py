from .type import UflType

class UflIntegerType(UflType):
    def __init__(self, default=None):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
    
    def __str__(self):
        return "Integer"
