from .tabs import *
from umlfri2.ufl.dialog.widgets import *
from ..types import *


class UflDialog:
    def __init__(self, type):
        self.__type = type
        self.__tabs = []
        if isinstance(self.__type, UflListType):
            self.__add_list_tab("General", self.__type)
        elif isinstance(self.__type, UflObjectType):
            self.__add_tabs()
        else:
            raise ValueError("UflDialog can be constructed using list or object type only")
    
    def __add_tabs(self):
        tab = UflDialogObjectTab("General")
        self.__tabs.append(tab)
        
        for name, type in self.__type.attributes:
            if isinstance(type, UflListType):
                self.__add_list_tab(name, type)
            elif isinstance(type, UflObjectType):
                self.__add_object_tab(name, type)
            else:
                tab.add_widget(self.__make_widget(tab, name, name, type))
    
    def __add_list_tab(self, name, type):
        tab = UflDialogListTab(name, type)
        self.__tabs.append(tab)
        
        if isinstance(type.item_type, UflObjectType):
            for name, attr_type in type.item_type.attributes:
                tab.add_widget(self.__make_widget(tab, name, name, attr_type))
        else:
            tab.add_widget(self.__make_widget(tab, None, None, type))
    
    def __add_object_tab(self, name, type):
        tab = UflDialogObjectTab(name)
        self.__tabs.append(tab)
        
        for name, attr_type in type.attributes:
            tab.add_widget(self.__make_widget(tab, name, name, attr_type))

    def __make_widget(self, tab, id, label, type):
        if isinstance(type, UflBoolType):
            return UflDialogCheckWidget(tab, id, label)
        elif isinstance(type, UflColorType):
            return UflDialogColorWidget(tab, id, label)
        elif isinstance(type, (UflDefinedEnumType, UflEnumType, UflTypedEnumType)):
            return UflDialogSelectWidget(tab, id, label, type.possibilities)
        elif isinstance(type, UflFontType):
            return UflDialogFontWidget(tab, id, label)
        elif isinstance(type, UflFontType):
            return UflDialogFontWidget(tab, id, label)
        elif isinstance(type, (UflObjectType, UflListType)):
            return UflDialogChildWidget(tab, id, label, UflDialog(type))
        elif isinstance(type, UflStringType):
            if type.multiline:
                return UflDialogTextAreaWidget(tab, id, label)
            elif type.possibilities:
                return UflDialogComboWidget(tab, id, label, type.possibilities)
            else:
                return UflDialogTextWidget(tab, id, label)
        else:
            raise ValueError
    
    @property
    def tabs(self):
        yield from self.__tabs
    
    def get_lonely_tab(self):
        if len(self.__tabs) == 1:
            return self.__tabs[0]
        else:
            return None
