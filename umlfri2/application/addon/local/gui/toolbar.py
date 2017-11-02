from uuid import uuid4


class ToolBar:
    def __init__(self, label, items):
        self.__label = label
        self.__items = tuple(items)
        self.__id = uuid4() # random ID for now
        self.__addon = None
    
    def _set_addon(self, addon):
        self.__addon = addon
    
    @property
    def addon(self):
        return self.__addon
    
    @property
    def id(self):
        return self.__id
    
    @property
    def label(self):
        return self.__label
    
    @property
    def items(self):
        yield from self.__items
