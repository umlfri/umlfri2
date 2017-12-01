from .type import UflType


class UflNumberType(UflType):
    _PYTHON_TYPE = None
    
    def __init__(self, default=None):
        self.__default = default or self._PYTHON_TYPE()
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        return self._PYTHON_TYPE(value)
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, self._PYTHON_TYPE)
    
    def is_default_value(self, value):
        return self.__default == value
    
    def is_equatable_to(self, other):
        return isinstance(other, UflNumberType)
    
    def is_comparable_with(self, other):
        return isinstance(other, UflNumberType)
    
    @property
    def is_convertable_to_string(self):
        return True
