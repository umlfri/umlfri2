from umlfri2.types.enums import ALL_ENUMS
from .typingvisitor import UflTypingVisitor
from .compilingvisitor import UflCompilingVisitor
from ..parser import parse_ufl


class CompiledUflExpression:
    __VARIABLE_PREFIX = 'ufl_'
    
    def __init__(self, expression, expected_type, variables):
        self.__source = expression
        
        tree = parse_ufl(expression)
        typing_visitor = UflTypingVisitor(variables, ALL_ENUMS, expected_type)
        
        typed_tree = tree.accept(typing_visitor)
        
        compiling_visitor = UflCompilingVisitor(self.__VARIABLE_PREFIX)
        self.__compiled_source = typed_tree.accept(compiling_visitor)
        self.__compiled_function = eval(self.compiled_source, compiling_visitor.all_globals)
        
        self.__parameters = tuple(var.name for var in typed_tree.variables)
        
        self.__type = typed_tree.type
    
    @property
    def source(self):
        return self.__source
    
    @property
    def parameters(self):
        yield from self.__parameters
    
    @property
    def compiled_source(self):
        return self.__compiled_source
    
    @property
    def compiled_function(self):
        return self.__compiled_function
    
    @property
    def type(self):
        return self.__type
