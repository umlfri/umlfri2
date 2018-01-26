from .node import UflNode


class UflMacroInvokeNode(UflNode):
    def __init__(self, target, selector, parameters, inner_type_invoke, macro=None, type=None):
        super().__init__(type)
        
        self.__target = target
        self.__selector = selector
        self.__parameters = parameters
        
        self.__inner_type_invoke = inner_type_invoke
        
        self.__macro = macro
    
    @property
    def target(self):
        return self.__target
    
    @property
    def selector(self):
        return self.__selector
    
    @property
    def parameters(self):
        return self.__parameters
    
    @property
    def macro(self):
        return self.__macro
    
    @property
    def inner_type_invoke(self):
        return self.__inner_type_invoke
    
    def _get_params(self):
        return (self.__target, self.__selector, 'inner' if self.__inner_type_invoke else 'outer') + tuple(self.__parameters)

    def accept(self, visitor):
        return visitor.visit_macro_invoke(self)
