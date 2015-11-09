from .type import UflType


class UflEnumType(UflType):
    def __init__(self, possibilities, default=None):
        self.__possibilities = tuple(possibilities)
        if default and default in self.__possibilities:
            self.__default = default
        else:
            self.__default = self.__possibilities[0]
    
    @property
    def default(self):
        return self.__default
    
    @property
    def possibilities(self):
        return self.__possibilities
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        if value not in self.__possibilities:
            raise ValueError("Invalid value")
        return value
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.__possibilities == other.possibilities
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return value in self.__possibilities
    
    def __str__(self):
        return 'Enum[{0}]'.format(", ".join(self.__possibilities))
