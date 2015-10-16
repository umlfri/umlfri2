from .type import UflType


class UflListType(UflType):
    def __init__(self, item_type):
        self.__item_type = item_type
    
    @property
    def item_type(self):
        return self.__item_type
    
    def build_default(self):
        return []
    
    def __str__(self):
        return "List<{0}>".format(self.__item_type)
