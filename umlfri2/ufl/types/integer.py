from .type import UflType

class UflIntegerType(UflType):
    def __init__(self, default=0):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self):
        return self.__default
    
    def parse(self, value):
        return int(value)
    
    def __str__(self):
        return "Integer"
