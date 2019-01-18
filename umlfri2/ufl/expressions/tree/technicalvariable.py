from .node import UflNode


class UflTechnicalVariableNode(UflNode):
    def __init__(self, name, type=None):
        super().__init__(type)
        
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    def _get_params(self):
        return self.__name,
    
    def accept(self, visitor):
        return visitor.visit_technical_variable(self)
