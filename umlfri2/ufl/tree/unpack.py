from .node import UflNode


class UflUnpackNode(UflNode):
    def __init__(self, object, type=None):
        super().__init__(type)
        
        self.__object = object
        
    @property
    def object(self):
        return self.__object
    
    def _get_params(self):
        return self.__object
    
    def accept(self, visitor):
        return visitor.visit_unpack(self)
