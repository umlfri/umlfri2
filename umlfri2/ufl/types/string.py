from .type import UflType


class UflStringType(UflType):
    def __init__(self, possibilities=None, default=None, multiline=False):
        self.__default = default
        if possibilities:
            self.__possibilities = tuple(possibilities)
        else:
            self.__possibilities = None
        self.__multiline = multiline
    
    @property
    def default(self):
        return self.__default
    
    @property
    def possibilities(self):
        return self.__possibilities
    
    @property
    def multiline(self):
        return self.__multiline
