from .node import UflNode


class UflLiteralNode(UflNode):
    def __init__(self, value, type=None):
        super().__init__(type)
        
        self.__value = value
    
    @property
    def value(self):
        return self.__value
    
    def _get_params(self):
        return self.__value,

    def accept(self, visitor):
        return visitor.visit_literal(self)
