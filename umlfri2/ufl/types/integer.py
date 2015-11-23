from .type import UflType

class UflIntegerType(UflType):
    def __init__(self, default=None):
        self.__default = default or 0
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        return int(value)
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, int)
    
    def is_default_value(self, value):
        return self.__default == value
    
    def __str__(self):
        return "Integer"
