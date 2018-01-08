from .expression import Expression
from umlfri2.ufl.compiler import CompiledUflExpression


class UflExpression(Expression):
    def __init__(self, expression):
        self.__expression = expression
        self.__compiled = None
    
    def compile(self, type_context, expected_type):
        self.__compiled = CompiledUflExpression(
            self.__expression,
            expected_type,
            type_context.as_dict()
        )
    
    def get_type(self):
        return self.__compiled.type
    
    def __call__(self, context):
        return self.__compiled.compiled_function(*context.get_variables(self.__compiled.parameters))
    
    def __repr__(self):
        return '<UflExpression "{0}" of type {1}>'.format(self.__expression, self.__compiled.type)
