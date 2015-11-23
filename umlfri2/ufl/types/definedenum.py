from .type import UflType


class UflDefinedEnumType(UflType):
    def __init__(self, type, possibilities={}, default=None):
        self.__possibilities = possibilities.copy()
        self.__type = type
        
        if default and default in self.__possibilities:
            self.__default = self.__possibilities[default]
        elif self.__possibilities:
            self.__default = iter(self.__possibilities).__next__()
        else:
            self.__default = None
    
    @property
    def default(self):
        return self.__default
    
    @property
    def possibilities(self):
        return self.__possibilities.keys()
    
    @property
    def name(self):
        return self.__type.__name__
    
    @property
    def type(self):
        return self.__type
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        return self.__possibilities[value]
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.__type == other.__type
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, self.__type)
    
    def is_default_value(self, value):
        return self.__default == value
    
    def __str__(self):
        return 'DefinedEnum[{0}]'.format(self.name)
