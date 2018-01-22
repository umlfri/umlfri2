from .valueprovider import ValueProvider
from ...expressions import CompiledUflExpression


class DynamicValueProvider(ValueProvider):
    def __init__(self, expression):
        self.__expression = expression
        self.__compiled = None
    
    def compile(self, type_context, expected_type):
        resolved_expected_type = type_context.resolve_defined_enum(expected_type)
        
        self.__compiled = CompiledUflExpression(
            self.__expression,
            resolved_expected_type,
            type_context.as_dict()
        )
        
        if not resolved_expected_type.is_assignable_from(self.__compiled.type):
            raise Exception("Invalid type: {0}, but {1} expected".format(self.__compiled.type, resolved_expected_type))
    
    def get_type(self):
        return self.__compiled.type
    
    def __call__(self, context):
        return self.__compiled.compiled_function(*context.get_variables(self.__compiled.parameters))
    
    def __repr__(self):
        if self.__compiled is None:
            return '<DynamicValueProvider "{0}" uncompiled>'.format(self.__expression)
        else:
            return '<DynamicValueProvider "{0}" of type {1}>'.format(self.__expression, self.__compiled.type)
