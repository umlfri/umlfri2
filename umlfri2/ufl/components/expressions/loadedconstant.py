from .expression import Expression


class LoadedConstantExpression(Expression):
    def __init__(self, value):
        self.__value = value
        self.__type = None
    
    def compile(self, type_context, expected_type):
        self.__type = type_context.resolve_defined_enum(expected_type)
        self.__value = self.__type.parse(self.__value)
    
    def get_type(self):
        return self.__type
    
    def __call__(self, context):
        return self.__value
    
    def __repr__(self):
        if self.__type is None:
            return "<LoadedExpression {0!r} unparsed>".format(self.__value, self.__type)
        else:
            return "<LoadedExpression {0!r} of type {1}>".format(self.__value, self.__type)
