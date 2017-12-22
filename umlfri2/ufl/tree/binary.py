from .node import UflNode



class UflBinaryNode(UflNode):
    def __init__(self, operand1, operator, operand2, type=None):
        super().__init__(type)
        
        self.__operand1 = operand1
        self.__operand2 = operand2
        self.__operator = operator
    
    @property
    def operand1(self):
        return self.__operand1
    
    @property
    def operand2(self):
        return self.__operand2
    
    @property
    def operator(self):
        return self.__operator
    
    def _get_params(self):
        return self.__operand1, self.__operator, self.__operand2

    def accept(self, visitor):
        return visitor.visit_binary(self)
