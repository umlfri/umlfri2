from .node import UflNode


class UflObjectMetadataAccessNode(UflNode):
    def __init__(self, obj, metadata_name, type=None):
        super().__init__(type)

        self.__object = obj
        self.__metadata_name = metadata_name
    
    @property
    def object(self):
        return self.__object
    
    @property
    def metadata_name(self):
        return self.__metadata_name
    
    def _get_params(self):
        return self.__object,
    
    def accept(self, visitor):
        return visitor.visit_object_metadata_access(self)
