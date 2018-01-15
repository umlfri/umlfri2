from .expression import Expression


class NoneConstantExpression(Expression):
    def __init__(self):
        self.__type = None
    
    def compile(self, type_context, expected_type):
        if self.__type is None:
            self.__type = type_context.resolve_defined_enum(expected_type)
    
    def get_type(self):
        return self.__type
    
    def __call__(self, context):
        return None
    
    def __repr__(self):
        return "<NoneConstantExpression of type {0}>".format(self.__type)
