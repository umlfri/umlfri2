from .enum import UflEnumType


class UflDefinedEnumType(UflEnumType):
    def __init__(self, type, possibilities={}, default=None):
        self.__possibilities = possibilities.copy()
        self.__type = type
        
        super().__init__(tuple(possibilities.keys()), default)
    
    @property
    def default(self):
        return self.__possibilities[self.default_item]
    
    @property
    def name(self):
        return self.__type.__name__
    
    @property
    def type(self):
        return self.__type
    
    def build_default(self, generator):
        return self.default
    
    def parse(self, value):
        return self.__possibilities[value]
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.__type == other.__type
    
    def is_valid_value(self, value):
        return isinstance(value, self.__type)
    
    def is_default_value(self, value):
        return self.default == value
    
    def __str__(self):
        return 'DefinedEnum[{0}]'.format(self.name)
