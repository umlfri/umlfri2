from .node import UflNode


class UflUnary(UflNode):
    def __init__(self, operator, operand):
        self.__operator = operator
        self.__operand = operand
    
    @property
    def operator(self):
        return self.__operator
    
    @property
    def operand(self):
        return self.__operand
    
    def _get_params(self):
        return self.__operator, self.__operand
    
    def accept(self, visitor):
        return visitor.visit_unary(self)
