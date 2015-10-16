from .type import UflType, UflMethodDescription
from .integer import UflIntegerType


class UflColorType(UflType):
    def __init__(self, default=None):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
    
    def __str__(self):
        return 'Color'

UflType.ALLOWED_DIRECT_ATTRIBUTES = {
    'r': ('r', UflIntegerType),
    'g': ('g', UflIntegerType),
    'b': ('b', UflIntegerType),
    'a': ('alpha', UflIntegerType),
}

UflColorType.ALLOWED_DIRECT_METHODS = {
    'invert': UflMethodDescription('invert', (), UflColorType),
}
