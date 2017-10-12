from umlfri2.types.enums import ALL_ENUMS
from .expression import Expression
from umlfri2.ufl.compiler import compile_ufl


class UflExpression(Expression):
    def __init__(self, expression):
        self.__expression = expression
        self.__compiled = None
        self.__type = None
    
    def compile(self, type_context, expected_type):
        self.__type, self.__compiled = compile_ufl(
            self.__expression,
            expected_type,
            type_context.as_dict(),
            ALL_ENUMS
        )
    
    def get_type(self):
        return self.__type
    
    def __call__(self, context):
        return self.__compiled(**context.as_dict())
