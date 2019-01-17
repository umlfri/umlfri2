from umlfri2.types.proportion import WHOLE_PROPORTION, Proportion

from ..base.type import UflType


class UflProportionType(UflType):
    def __init__(self, default=None):
        self.__default = default or WHOLE_PROPORTION
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        return Proportion.from_string(value)
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        if not isinstance(value, Proportion):
            return False
        
        return True
    
    def is_default_value(self, value):
        return self.__default == value
    
    def __str__(self):
        return 'Proportion'
