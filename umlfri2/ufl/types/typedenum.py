from .type import UflType


class UflTypedEnumType(UflType):
    def __init__(self, type, default=None):
        self.__possibilities = tuple(i for i in dir(type) if not i.startswith('_'))
        self.__type = type
        
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
    
    @property
    def name(self):
        return self.__type.__name__
    
    @property
    def type(self):
        return self.__type
    
    def build_default(self, generator):
        return getattr(self.__type, self.__default)
    
    def parse(self, value):
        return getattr(self.__type, value)
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.__type == other.__type
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, int) # TODO: Python 3.4: self.__type
    
    def __str__(self):
        return 'TypedEnum[{0}]'.format(self.name)
