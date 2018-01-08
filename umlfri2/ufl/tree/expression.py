from .node import UflNode


class UflExpressionNode(UflNode):
    def __init__(self, result, variable_types=None, type=None):
        super().__init__(type)
        
        self.__result = result
        self.__variable_types = variable_types
        if variable_types is None:
            self.__variables = None
        else:
            self.__variables = tuple(variable_types.keys())
    
    @property
    def result(self):
        return self.__result
    
    @property
    def variable_types(self):
        return self.__variable_types.copy()
    
    @property
    def variables(self):
        return self.__variables
    
    def _get_params(self):
        return self.__result,
    
    def accept(self, visitor):
        return visitor.visit_expression(self)
