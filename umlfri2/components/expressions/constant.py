from .expression import Expression
from umlfri2.types.color import Color
from umlfri2.types.font import Font
from umlfri2.ufl.types import UflIntegerType, UflStringType, UflColorType, UflFontType


class ConstantExpression(Expression):
    __types = {
        int: UflIntegerType(),
        str: UflStringType(),
        Color: UflColorType(),
        Font: UflFontType(),
        type(None): None,
    }
    
    def __init__(self, value, value_type=None):
        self.__value = value
        if value_type is None:
            self.__type = self.__types[type(value)]
        else:
            self.__type = value_type
    
    def compile(self, variables, expected_type):
        pass
    
    def get_type(self):
        return self.__type
    
    def __call__(self, context):
        return self.__value

NoneExpression = ConstantExpression(None)
