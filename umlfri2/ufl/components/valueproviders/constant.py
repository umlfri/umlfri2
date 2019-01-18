from .compilationerror import ValueCompilationError
from .valueprovider import ValueProvider


class ConstantValueProvider(ValueProvider):
    def __init__(self, value, source=None):
        self.__value = value
        self.__type = None
        self.__source = source
    
    def compile(self, type_context, expected_type):
        try:
            self.__type = type_context.resolve_defined_enum(expected_type)
            self.__value = self.__type.parse(self.__value)
        except Exception as e:
            raise ValueCompilationError(self.__source) from e
    
    def get_type(self):
        return self.__type
    
    def get_source(self):
        return self.__source
    
    def __call__(self, context):
        return self.__value
    
    def __repr__(self):
        if self.__type is None:
            return "<ConstantValueProvider {0!r} unparsed>".format(self.__value, self.__type)
        else:
            return "<ConstantValueProvider {0!r} of type {1}>".format(self.__value, self.__type)
