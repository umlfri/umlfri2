from .node import UflNode


class UflLiteral(UflNode):
    def __init__(self, value):
        self.__value = value
    
    @property
    def value(self):
        return self.__value
    
    def _get_params(self):
        return self.__value,

    def accept(self, visitor):
        return visitor.visit_literal(self)
