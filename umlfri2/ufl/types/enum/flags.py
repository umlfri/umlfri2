from collections import OrderedDict

from ...objects import UflFlags
from ..base.type import UflType


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
    
    def build_default(self, generator):
        default = set()
        for possibility in self.__default:
            default.add(possibility.value)
        return UflFlags(self, default)
    
    @property
    def possibilities(self):
        return self.__possibilities.values()
    
    @property
    def is_immutable(self):
        return False

    @property
    def item_type(self):
        raise NotImplementedError
    
    def parse(self, value):
        return UflFlags(self, set(self.__possibilities[item].value for item in value.split()))
    
    def parse_possibility(self, value):
        return self.__possibilities[value].value
    
    def is_valid_possibility(self, value):
        for possibility in self.__possibilities.values():
            if possibility.value == value:
                return True
        return False
    
    def is_default_value(self, value):
        for possibility in self.__possibilities.values():
            if possibility in self.__default and possibility.value not in value:
                return False
            if possibility not in self.__default and possibility.value in value:
                return False
        return True
