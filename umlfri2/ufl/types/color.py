from .type import UflType, UflMethodDescription, UflAttributeDescription
from .integer import UflIntegerType
from umlfri2.types.color import Colors, Color


class UflColorType(UflType):
    def __init__(self, default=None):
        self.__default = default or Colors.black
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        return Color.from_string(value)
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, Color)
    
    def is_default_value(self, value):
        return self.__default == value
    
    def __str__(self):
        return 'Color'


UflColorType.ALLOWED_DIRECT_ATTRIBUTES = {
    'r': UflAttributeDescription('r', UflIntegerType()),
    'g': UflAttributeDescription('g', UflIntegerType()),
    'b': UflAttributeDescription('b', UflIntegerType()),
    'a': UflAttributeDescription('alpha', UflIntegerType()),
}
