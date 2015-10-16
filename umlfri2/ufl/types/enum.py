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
    
    def build_default(self):
        return self.__default
    
    def __str__(self):
        return 'Enum[{0}]'.format(", ".join(self.__possibilities))
