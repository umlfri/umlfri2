from .type import UflType, UflMethodDescription, UflAttributeDescription
from .integer import UflIntegerType
from .string import UflStringType
from .typedenum import UflTypedEnumType
from umlfri2.types.font import FontStyle, Font, Fonts
from umlfri2.ufl.types import UflBoolType


class UflFontType(UflType):
    def __init__(self, default=None):
        self.__default = default or Fonts.default
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        return Font.get_font(value)
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, Font)
    
    def is_default_value(self, value):
        return self.__default == value
    
    def __str__(self):
        return "Font"

UflFontType.ALLOWED_DIRECT_ATTRIBUTES = {
    'size': UflAttributeDescription('size', UflIntegerType()),
    'style': UflAttributeDescription('style', UflTypedEnumType(FontStyle)),
    'family': UflAttributeDescription('family', UflStringType()),
}

UflFontType.ALLOWED_DIRECT_METHODS = {
    'change': UflMethodDescription(
        'change',
        (UflTypedEnumType(FontStyle), UflBoolType()),
        UflFontType()
    )
}
