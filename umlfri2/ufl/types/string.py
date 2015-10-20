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
    
    def build_default(self):
        return ''
    
    def parse(self, value):
        return value
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, str)
    
    def __str__(self):
        return 'String'
