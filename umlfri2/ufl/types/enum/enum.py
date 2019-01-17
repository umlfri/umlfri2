from collections import OrderedDict

from ..base.type import UflType


class UflEnumType(UflType):
    def __init__(self, possibilities, default=None):
        self.__possibilities = OrderedDict((item.name, item) for item in possibilities)
        
        if default is not None:
            self.__default = self.__possibilities[default]
        elif self.__possibilities:
            self.__default = next(iter(self.__possibilities.values()))
        else:
            self.__default = None
    
    @property
    def default_possibility(self):
        return self.__default
    
    @property
    def default(self):
        return self.__default.value
    
    def build_default(self, generator):
        return self.default
    
    @property
    def possibilities(self):
        return self.__possibilities.values()
    
    @property
    def is_immutable(self):
        return True
    
    def parse(self, value):
        return self.__possibilities[value].value
    
    def is_valid_value(self, value):
        for possibility in self.__possibilities.values():
            if possibility.value == value:
                return True
        return False
    
    def is_valid_item(self, item):
        return item in self.__possibilities
    
    def is_default_value(self, value):
        return self.default == value
