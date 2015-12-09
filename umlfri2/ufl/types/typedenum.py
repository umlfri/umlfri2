from .enum import UflEnumType


class UflTypedEnumType(UflEnumType):
    def __init__(self, type, default=None):
        possibilities = tuple(i for i in dir(type) if not i.startswith('_'))
        self.__type = type
        
        super().__init__(possibilities, default)
        
        self.__default = getattr(self.__type, self.default_item)
    
    @property
    def default(self):
        return self.__default
    
    @property
    def name(self):
        return self.__type.__name__
    
    @property
    def type(self):
        return self.__type
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        return getattr(self.__type, value)
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.possibilities == other.possibilities
    
    def is_valid_value(self, value):
        return isinstance(value, int) # TODO: Python 3.4: self.__type
    
    def is_default_value(self, value):
        return self.__default == value
    
    def __str__(self):
        return 'TypedEnum[{0}]'.format(self.name)
