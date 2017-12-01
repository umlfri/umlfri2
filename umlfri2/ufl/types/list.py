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
    
    def is_assignable_from(self, other):
        if not isinstance(other, UflListType):
            return False
        
        return self.__item_type.is_assignable_from(other.__item_type)
    
    def is_default_value(self, value):
        return value.get_length() == 0
    
    @property
    def is_immutable(self):
        return False
    
    def set_parent(self, parent):
        super().set_parent(parent)
        self.__item_type.set_parent(self)
    
    def __str__(self):
        return "List<{0}>".format(self.__item_type)
