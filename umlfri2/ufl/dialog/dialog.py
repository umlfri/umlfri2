from .options import UflDialogOptions
from ..objects.mutable import UflMutable
from .tabs import *
from .columns import *
from .widgets import *
from ..types import *


class UflDialog:
    def __init__(self, type, options=UflDialogOptions.standard):
        self.__type = type
        self.__tabs = []
        self.__original_object = None
        self.__mutable_object = None
        self.__options = options
        self.__current_tab = None
        if isinstance(self.__type, UflListType):
            self.__current_tab = self.__add_list_tab(None, self.__type)
        elif isinstance(self.__type, UflObjectType):
            self.__add_tabs()
        else:
            raise ValueError("UflDialog can be constructed using list or object type only")
        
        for no, tab in enumerate(self.__tabs):
            tab._associate_tab_index(no)
    
    def __add_tabs(self):
        tab = UflDialogObjectTab(None)
        self.__tabs.append(tab)
        
        for attr in self.__type.attributes:
            if self.__options.list_as_tab and isinstance(attr.type, UflListType):
                self.__add_list_tab(attr, attr.type)
            elif self.__options.multiline_as_tab and isinstance(attr.type, UflStringType) and attr.type.multiline:
                self.__add_multiline_tab(attr, attr.type)
            elif self.__options.object_as_tab and isinstance(attr.type, UflObjectType):
                self.__add_object_tab(attr, attr.type)
            else:
                tab.add_widget(self.__make_widget(tab, attr, attr.type))
        
        if self.__tabs[0].widget_count == 0:
            del self.__tabs[0]
        
        if self.__tabs:
            self.__current_tab = self.__tabs[0]
    
    def __add_list_tab(self, attr, type):
        tab = UflDialogListTab(attr, type)
        self.__tabs.append(tab)
        
        if isinstance(type.item_type, UflObjectType):
            for attr in type.item_type.attributes:
                tab.add_column(self.__make_column(attr, attr.type))
                tab.add_widget(self.__make_widget(tab, attr, attr.type))
        else:
            tab.add_column(self.__make_column(None, type.item_type))
            tab.add_widget(self.__make_widget(tab, None, type.item_type))
        
        return tab
    
    def __add_object_tab(self, attr, type):
        tab = UflDialogObjectTab(attr)
        self.__tabs.append(tab)
        
        for attr in type.attributes:
            tab.add_widget(self.__make_widget(tab, attr, attr.type))
        
        return tab
    
    def __add_multiline_tab(self, attr, type):
        tab = UflDialogValueTab(attr)
        self.__tabs.append(tab)
        
        tab.add_widget(self.__make_widget(tab, None, type))
        
        return tab

    def __make_column(self, attr, type):
        if isinstance(type, UflBoolType):
            return UflDialogCheckColumn(attr)
        elif isinstance(type, UflEnumType):
            return UflDialogEnumColumn(attr)
        elif isinstance(type, (UflObjectType, UflListType)):
            return UflDialogComplexColumn(attr)
        elif isinstance(type, UflStringType) and type.multiline:
            return UflDialogComplexColumn(attr)
        else:
            return UflDialogValuedColumn(attr)
        
    def __make_widget(self, tab, attr, type):
        if isinstance(type, UflBoolType):
            return UflDialogCheckWidget(tab, attr)
        elif isinstance(type, UflColorType):
            return UflDialogColorWidget(tab, attr)
        elif isinstance(type, UflEnumType):
            return UflDialogSelectWidget(tab, attr)
        elif isinstance(type, UflFlagsType):
            return UflDialogMultiSelectWidget(tab, attr)
        elif isinstance(type, UflFontType):
            return UflDialogFontWidget(tab, attr)
        elif isinstance(type, UflIntegerType):
            return UflDialogIntegerWidget(tab, attr)
        elif isinstance(type, UflDecimalType):
            return UflDialogDecimalWidget(tab, attr)
        elif isinstance(type, (UflObjectType, UflListType)):
            return UflDialogChildWidget(tab, attr, UflDialog(type, self.__options))
        elif isinstance(type, UflStringType):
            if type.multiline:
                return UflDialogTextAreaWidget(tab, attr)
            elif type.possibilities:
                return UflDialogComboWidget(tab, attr)
            else:
                return UflDialogTextWidget(tab, attr)
        else:
            raise ValueError
    
    @property
    def should_save_tab(self):
        return isinstance(self.__current_tab, UflDialogListTab) and self.__current_tab.should_save
    
    def switch_tab(self, index):
        if isinstance(self.__current_tab, UflDialogListTab):
            if self.__current_tab.should_save:
                raise Exception
            
            self.__current_tab.tab_deselected()
        
        self.__current_tab = self.__tabs[index]
    
    @property
    def current_tab(self):
        return self.__current_tab
    
    @property
    def original_object(self):
        return self.__original_object
    
    def finish(self):
        for tab in self.__tabs:
            tab.finish()
            if isinstance(tab, UflDialogValueTab):
                self.__mutable_object.set_value(tab.id, tab.current_object)
    
    def make_patch(self):
        if self.__mutable_object is None:
            return None
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
            self.__original_object = None
            self.__mutable_object = None
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
    
    def refresh(self):
        self.associate(self.__original_object)
    
    def translate(self, translation):
        for tab in self.__tabs:
            tab.translate(translation)
    
    def reset(self):
        if self.__original_object is None:
            raise Exception
        
        self.__mutable_object = self.__original_object.make_mutable()
        for tab in self.__tabs:
            if tab.id is None:
                tab.associate(self.__mutable_object)
            else:
                tab.associate(self.__mutable_object.get_value(tab.id))
