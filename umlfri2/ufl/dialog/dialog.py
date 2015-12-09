from .options import UflDialogOptions
from ..objects.mutable import UflMutable
from .tabs import *
from umlfri2.ufl.dialog.widgets import *
from ..types import *


class UflDialog:
    def __init__(self, type, translation, options=UflDialogOptions.standard):
        self.__type = type
        self.__translation = translation
        self.__tabs = []
        self.__original_object = None
        self.__mutable_object = None
        self.__options = options
        if isinstance(self.__type, UflListType):
            self.__add_list_tab(None, None, self.__type)
        elif isinstance(self.__type, UflObjectType):
            self.__add_tabs()
        else:
            raise ValueError("UflDialog can be constructed using list or object type only")
    
    def __add_tabs(self):
        tab = UflDialogObjectTab(None, None)
        self.__tabs.append(tab)
        
        for attr in self.__type.attributes:
            tab_label = self.__translation.translate(attr)
            if self.__options.list_as_tab and isinstance(attr.type, UflListType):
                self.__add_list_tab(attr.name, tab_label, attr.type)
            elif self.__options.multiline_as_tab and isinstance(attr.type, UflStringType) and attr.type.multiline:
                self.__add_multiline_tab(attr.name, tab_label, attr.type)
            elif self.__options.object_as_tab and isinstance(attr.type, UflObjectType):
                self.__add_object_tab(attr.name, tab_label, attr.type)
            else:
                tab.add_widget(self.__make_widget(tab, attr.name, tab_label, attr.type))
    
    def __add_list_tab(self, id, name, type):
        tab = UflDialogListTab(id, name, type)
        self.__tabs.append(tab)
        
        if isinstance(type.item_type, UflObjectType):
            for attr in type.item_type.attributes:
                label = self.__translation.translate(attr)
                tab.add_widget(self.__make_widget(tab, attr.name, label, attr.type))
        else:
            tab.add_widget(self.__make_widget(tab, None, None, type))
    
    def __add_object_tab(self, id, name, type):
        tab = UflDialogObjectTab(id, name)
        self.__tabs.append(tab)
        
        for attr in type.attributes:
            label = self.__translation.translate(attr)
            tab.add_widget(self.__make_widget(tab, attr.name, label, attr.type))
    
    def __add_multiline_tab(self, id, name, type):
        tab = UflDialogValueTab(id, name)
        self.__tabs.append(tab)
        
        tab.add_widget(self.__make_widget(tab, None, None, type))

    def __make_widget(self, tab, id, label, type):
        if isinstance(type, UflBoolType):
            return UflDialogCheckWidget(tab, id, label)
        elif isinstance(type, UflColorType):
            return UflDialogColorWidget(tab, id, label)
        elif isinstance(type, (UflDefinedEnumType, UflListEnumType, UflTypedEnumType)):
            return UflDialogSelectWidget(tab, id, label, type.possibilities)
        elif isinstance(type, UflFontType):
            return UflDialogFontWidget(tab, id, label)
        elif isinstance(type, UflFontType):
            return UflDialogFontWidget(tab, id, label)
        elif isinstance(type, (UflObjectType, UflListType)):
            return UflDialogChildWidget(tab, id, label, UflDialog(type, self.__translation, self.__options))
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
    def original_object(self):
        return self.__original_object
    
    def finish(self):
        for tab in self.__tabs:
            tab.finish()
            if isinstance(tab, UflDialogValueTab):
                self.__mutable_object.set_value(tab.id, tab.current_object)
    
    def make_patch(self):
        return self.__mutable_object.make_patch()
    
    @property
    def tabs(self):
        yield from self.__tabs
    
    def get_lonely_tab(self):
        if len(self.__tabs) == 1:
            return self.__tabs[0]
        else:
            return None
    
    def associate(self, ufl_object):
        if ufl_object is None:
            for tab in self.__tabs:
                tab.associate(None)
        else:
            if not isinstance(ufl_object, UflMutable):
                self.__original_object = ufl_object
                ufl_object = ufl_object.make_mutable()
            else:
                self.__original_object = None
            
            if ufl_object.type is not self.__type:
                raise ValueError
            
            self.__mutable_object = ufl_object
            
            for tab in self.__tabs:
                if tab.id is None:
                    tab.associate(ufl_object)
                else:
                    tab.associate(ufl_object.get_value(tab.id))
    
    def reset(self):
        if self.__original_object is None:
            raise Exception
        
        self.__mutable_object = self.__original_object.make_mutable()
        for tab in self.__tabs:
            if tab.id is None:
                tab.associate(self.__mutable_object)
            else:
                tab.associate(self.__mutable_object.get_value(tab.id))
