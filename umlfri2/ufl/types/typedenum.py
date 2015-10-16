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
    
    def build_default(self):
        return getattr(self.__type, self.__default)
    
    def __str__(self):
        return 'TypedEnum[{0}]'.format(self.name)
