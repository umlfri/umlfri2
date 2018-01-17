from .node import UflNode


class UflEnumNode(UflNode):
    def __init__(self, enum, item, type=None):
        super().__init__(type)
        
        self.__enum = enum
        self.__item = item
    
    @property
    def enum(self):
        return self.__enum
    
    @property
    def item(self):
        return self.__item
    
    def _get_params(self):
        return self.__enum, self.__item

    def accept(self, visitor):
        return visitor.visit_enum(self)
