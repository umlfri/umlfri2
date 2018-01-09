from .node import UflNode


class UflExpressionNode(UflNode):
    def __init__(self, result, variables, type=None):
        super().__init__(type)
        
        self.__result = result
        self.__variables = variables
    
    @property
    def result(self):
        return self.__result
    
    @property
    def variables(self):
        yield from self.__variables
    
    def _get_params(self):
        return self.__result,
    
    def accept(self, visitor):
        return visitor.visit_expression(self)
