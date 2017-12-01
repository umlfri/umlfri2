from .expression import Expression
from umlfri2.types.color import Color
from umlfri2.types.font import Font
from umlfri2.ufl.types import UflIntegerType, UflStringType, UflColorType, UflFontType, UflAnyType, UflNullableType


class ConstantExpression(Expression):
    __types = {
        int: UflIntegerType(),
        str: UflStringType(),
        Color: UflColorType(),
        Font: UflFontType(),
        type(None): UflNullableType(UflAnyType()),
    }
    
    def __init__(self, value, value_type=None):
        self.__value = value
        if value_type is None:
            self.__type = self.__types[type(value)]
        else:
            self.__type = value_type
    
    def compile(self, type_context, expected_type):
        if isinstance(self.__type, UflAnyType):
            self.__type = expected_type
            self.__value = expected_type.parse(self.__value)
        elif self.__value is None and isinstance(expected_type, UflNullableType):
            self.__type = expected_type
    
    def get_type(self):
        return self.__type
    
    def change_type(self, type):
        if isinstance(self.__type, UflAnyType):
            value = type.parse(self.__value)
        else:
            value = self.__value
        
        return ConstantExpression(value, type)
    
    def __call__(self, context):
        return self.__value
    
    def __repr__(self):
        return "<ConstantExpression {0!r} of type {1}>".format(self.__value, self.__type)

NoneExpression = ConstantExpression(None)
