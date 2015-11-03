from .expression import Expression
from umlfri2.ufl.compiler import compile_ufl
from ..visual.align import HorizontalAlignment, VerticalAlignment
from ..visual.line import LineOrientation
from umlfri2.types.font import FontStyle


class UflExpression(Expression):
    __enums = {
        'FontStyle': FontStyle,
        'HorizontalAlignment': HorizontalAlignment,
        'VerticalAlignment': VerticalAlignment,
        'LineOrientation': LineOrientation,
    }
    
    def __init__(self, expression):
        self.__expression = expression
        self.__compiled = None
        self.__type = None
    
    def compile(self, variables, expected_type):
        self.__type, self.__compiled = compile_ufl(self.__expression, expected_type, variables, self.__enums)
    
    def get_type(self):
        return self.__type
    
    def __call__(self, context):
        return self.__compiled(**context.as_dict())
