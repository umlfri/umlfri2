from .node import UflNode


class UflLambdaExpressionNode(UflNode):
    def __init__(self, body, parameters, type=None):
        super().__init__(type)

        self.__body = body
        self.__parameters = tuple(parameters)
    
    @property
    def body(self):
        return self.__body
    
    @property
    def parameter_count(self):
        return len(self.__parameters)
    
    @property
    def parameters(self):
        yield from self.__parameters
    
    def _get_params(self):
        return self.__parameters, self.__body,
    
    def accept(self, visitor):
        return visitor.visit_lambda_expression(self)
