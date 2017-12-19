from .type import UflType


class UflBoolType(UflType):
    def __init__(self, default=None):
        self.__default = default or False
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        if value not in ('true', 'false'):
            raise ValueError("The given value is not boolean")
        return value == 'true'
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, bool)
    
    def is_default_value(self, value):
        return self.__default == value
    
    def is_equatable_to(self, other):
        return isinstance(other, UflBoolType)
    
    def __str__(self):
        return 'Bool'
