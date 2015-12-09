from .type import UflType


class UflEnumType(UflType):
    def __init__(self, possibilities, default=None):
        self.__possibilities = tuple(possibilities)
        if default and default in self.__possibilities:
            self.__default = default
        elif self.__possibilities:
            self.__default = self.__possibilities[0]
        else:
            self.__default = None
    
    @property
    def default_item(self):
        return self.__default
    
    @property
    def possibilities(self):
        return self.__possibilities
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_item(self, item):
        return item in self.__possibilities
