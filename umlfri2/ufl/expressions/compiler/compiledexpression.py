from umlfri2.types.enums import ALL_ENUMS
from .typingvisitor import UflTypingVisitor
from .compilingvisitor import UflCompilingVisitor
from ..parser import parse_ufl


class CompiledUflExpression:
    __VARIABLE_PREFIX = 'ufl_'
    
    def __init__(self, expression, expected_type, variables):
        tree = parse_ufl(expression)
        typing_visitor = UflTypingVisitor(variables, ALL_ENUMS, expected_type)
        
        self.__variables = variables
        
        self.__typed_tree = tree.accept(typing_visitor)
        
        self.__source = expression
        self.__compiled_source = None
        self.__compiled_function = None
    
    @property
    def source(self):
        return self.__source
    
    @property
    def parameters(self):
        for var in self.__typed_tree.variables:
            yield var.name
    
    @property
    def compiled_source(self):
        if self.__compiled_source is None:
            compiling_visitor = UflCompilingVisitor(self.__VARIABLE_PREFIX)
            self.__compiled_source = self.__typed_tree.accept(compiling_visitor)
        
        return self.__compiled_source
    
    @property
    def compiled_function(self):
        if self.__compiled_function is None:
            self.__compiled_function = eval(self.compiled_source, ALL_ENUMS.copy())
        return self.__compiled_function
    
    @property
    def type(self):
        return self.__typed_tree.type
