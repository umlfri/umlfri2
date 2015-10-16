from .type import UflType, UflMethodDescription
from .integer import UflIntegerType
from .string import UflStringType
from .typedenum import UflTypedEnumType
from umlfri2.types.font import FontStyle, Font


class UflFontType(UflType):
    def __init__(self, default=None):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self):
        return self.__default or Font('Arial', 10)
    
    def __str__(self):
        return "Font"

UflFontType.ALLOWED_DIRECT_ATTRIBUTES = {
    'size': ('size', UflIntegerType),
    'style': ('style', UflTypedEnumType(FontStyle)),
    'family': ('family', UflStringType),
}

UflFontType.ALLOWED_DIRECT_METHODS = {
    'change': UflMethodDescription(
        'change',
        (UflStringType, UflTypedEnumType(FontStyle)),
        UflFontType
    )
}
