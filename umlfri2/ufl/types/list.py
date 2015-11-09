from .type import UflType
from ..objects import UflList


class UflListType(UflType):
    def __init__(self, item_type):
        self.__item_type = item_type
    
    @property
    def item_type(self):
        return self.__item_type
    
    def build_default(self, generator):
        return UflList(self)
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.__item_type.is_same_as(other.__item_type)
    
    @property
    def is_immutable(self):
        return False
    
    def __str__(self):
        return "List<{0}>".format(self.__item_type)
