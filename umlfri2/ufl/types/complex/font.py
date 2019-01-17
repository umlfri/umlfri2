from umlfri2.ufl.types.base.type import UflType, UflAttributeDescription
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.enum.typedenum import UflTypedEnumType
from umlfri2.types.font import FontStyle, Font, Fonts


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
