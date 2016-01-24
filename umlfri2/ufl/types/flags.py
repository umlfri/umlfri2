from collections import OrderedDict

from .type import UflType


class UflFlagsType(UflType):
    def __init__(self, possibilities, default=None):
        self.__possibilities = OrderedDict((item.name, item) for item in possibilities)
        
        if default is not None:
            self.__default = tuple(self.__possibilities[item] for item in default)
        else:
            self.__default = ()
    
    @property
    def default_possibilities(self):
        yield from self.__default
    
    @property
    def default(self):
        for possibility in self.__default:
            yield possibility.value
    
    def build_default(self, generator):
        return set(self.default)
    
    @property
    def possibilities(self):
        return self.__possibilities.values()
    
    @property
    def is_immutable(self):
        return False
    
    def parse(self, value):
        return tuple(self.__possibilities[item].value for item in value.split())
    
    def is_valid_possibility(self, value):
        for possibility in self.__possibilities.values():
            if possibility.value == value:
                return True
        return False
    
    def is_default_value(self, value):
        return list(self.default) == value
