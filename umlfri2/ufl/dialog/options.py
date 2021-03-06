from enum import Enum


class UflDialogOptions(Enum):
    standard = (True, True, False)
    list = (False, False, True)
    
    def __init__(self, list_as_tab, object_as_tab, multiline_as_tab):
        self.__list_as_tab = list_as_tab
        self.__object_as_tab = object_as_tab
        self.__multiline_as_tab = multiline_as_tab
    
    @property
    def list_as_tab(self):
        return self.__list_as_tab
    
    @property
    def object_as_tab(self):
        return self.__object_as_tab
    
    @property
    def multiline_as_tab(self):
        return self.__multiline_as_tab
