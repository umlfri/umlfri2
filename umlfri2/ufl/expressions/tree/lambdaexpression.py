from .node import UflNode


class UflLambdaExpressionNode(UflNode):
    def __init__(self, result, parameters, type=None):
        super().__init__(type)

        self.__result = result
        self.__parameters = tuple(parameters)
    
    @property
    def result(self):
        return self.__result
    
    @property
    def parameters(self):
        yield from self.__parameters
    
    def _get_params(self):
        return self.__parameters, self.__result,
    
    def accept(self, visitor):
        return visitor.visit_lambda_expression(self)
