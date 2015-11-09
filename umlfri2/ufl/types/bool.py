from .type import UflType


class UflBoolType(UflType):
    def __init__(self, default=False):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        return value.lower() == 'true'
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, bool)
    
    def __str__(self):
        return 'Bool'
