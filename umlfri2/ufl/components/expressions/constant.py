from umlfri2.types.proportion import Proportion
from .expression import Expression

from umlfri2.types.enums import ALL_ENUMS
from umlfri2.types.color import Color
from umlfri2.types.font import Font
from umlfri2.ufl.types import UflIntegerType, UflStringType, UflColorType, UflFontType, UflTypedEnumType, \
    UflProportionType


class ConstantExpression(Expression):
    __types = {
        int: UflIntegerType(),
        str: UflStringType(),
        Color: UflColorType(),
        Font: UflFontType(),
        Proportion: UflProportionType(),
        **{x: UflTypedEnumType(x) for x in ALL_ENUMS.values()}
    }
    
    def __init__(self, value):
        self.__value = value
        self.__type = self.__types[type(value)]
    
    def compile(self, type_context, expected_type):
        resolved_expected_type = type_context.resolve_defined_enum(expected_type)
        
        if resolved_expected_type.is_assignable_from(self.__type):
            self.__type = resolved_expected_type
    
    def get_type(self):
        return self.__type
    
    def __call__(self, context):
        return self.__value
    
    def __repr__(self):
        return "<ConstantExpression {0!r} of type {1}>".format(self.__value, self.__type)
