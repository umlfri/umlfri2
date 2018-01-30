import linecache

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
        all_globals = compiling_visitor.all_globals

        self.__compiled_function = self.__compile(all_globals)
        
        self.__parameters = tuple(var.name for var in typed_tree.variables)
        
        self.__type = typed_tree.type
    
    def __compile(self, all_globals):
        temp_file_name = "ufl_{0}".format(id(self))
        
        to_eval = compile(self.__compiled_source, temp_file_name, "eval")
        
        linecache.cache[temp_file_name] = (
            1,
            None,
            ["{0} # ufl: {1}".format(self.__compiled_source, self.__source)],
            temp_file_name
        )

        return eval(to_eval, all_globals)
    
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
