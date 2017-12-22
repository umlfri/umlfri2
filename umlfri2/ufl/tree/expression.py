from .node import UflNode


class UflExpressionNode(UflNode):
    def __init__(self, result, type=None):
        super().__init__(type)

        self.__result = result
    
    @property
    def result(self):
        return self.__result
    
    def _get_params(self):
        return self.__result,
    
    def accept(self, visitor):
        return visitor.visit_expression(self)
