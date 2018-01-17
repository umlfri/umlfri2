from .node import UflNode


class UflAttributeAccessNode(UflNode):
    def __init__(self, obj, attribute, type=None):
        super().__init__(type)
        
        self.__object = obj
        self.__attribute = attribute
    
    @property
    def object(self):
        return self.__object
    
    @property
    def attribute(self):
        return self.__attribute
    
    def _get_params(self):
        return self.__object, self.__attribute

    def accept(self, visitor):
        return visitor.visit_attribute_access(self)
