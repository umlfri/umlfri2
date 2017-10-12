from .node import UflNode


class UflMetadataAccess(UflNode):
    def __init__(self, obj):
        self.__object = obj
    
    @property
    def object(self):
        return self.__object
    
    def _get_params(self):
        return self.__object,
    
    def accept(self, visitor):
        return visitor.visit_metadata_access(self)
