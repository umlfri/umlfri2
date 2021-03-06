from .node import UflNode


class UflVariableMetadataAccessNode(UflNode):
    def __init__(self, obj, type=None):
        super().__init__(type)
        
        self.__object = obj
    
    @property
    def object(self):
        return self.__object
    
    def _get_params(self):
        return self.__object,
    
    def accept(self, visitor):
        return visitor.visit_variable_metadata_access(self)
