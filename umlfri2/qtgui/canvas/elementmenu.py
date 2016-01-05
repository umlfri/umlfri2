from PySide.QtGui import QKeySequence

from umlfri2.application import Application
from umlfri2.application.commands.diagram import HideElementsCommand
from umlfri2.application.commands.model import DeleteElementsCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT
from ..base.contextmenu import ContextMenu
from ..properties import PropertiesDialog


class CanvasElementMenu(ContextMenu):
    def __init__(self, main_window, drawing_area, elements):
        super().__init__()
        
        self.__main_window = main_window
        self.__elements = tuple(elements)
        self.__diagram = drawing_area.diagram
        
        something_above = False
        something_below = False
        for element in self.__elements:
            if self.__diagram.is_something_above(Application().ruler, element):
                something_above = True
            if self.__diagram.is_something_below(Application().ruler, element):
                something_below = True
        
        self._add_menu_item(None, _("Hide"), QKeySequence.Delete, self.__hide)
        self._add_menu_item("edit-delete", _("Delete"), DELETE_FROM_PROJECT, self.__delete)
        
        self.addSeparator()
        
        if len(self.__elements) == 1:
            self._add_menu_item(None, _("Find in the project tree"), None, self.__show_in_project)
        else:
            self._add_menu_item(None, _("Find in the project tree"), None)
        
        if something_above or something_below:
            z_order_menu = self._add_sub_menu_item(_("Z-order"))
            
            if something_below:
                self._add_menu_item("go-down", _("Send back"), "PgDown", self.__zorder_back, z_order_menu)
            else:
                self._add_menu_item("go-down", _("Send back"), "PgDown", None, z_order_menu)
            
            if something_above:
                self._add_menu_item("go-up", _("Bring forward"), "PgUp", self.__zorder_forward, z_order_menu)
            else:
                self._add_menu_item("go-up", _("Bring forward"), "PgUp", None, z_order_menu)
            
            if something_below:
                self._add_menu_item("go-bottom", _("Send to bottom"), "End", self.__zorder_bottom, z_order_menu)
            else:
                self._add_menu_item("go-bottom", _("Send to bottom"), "End", None, z_order_menu)
            
            if something_above:
                self._add_menu_item("go-top", _("Bring to top"), "Home", self.__zorder_top, z_order_menu)
            else:
                self._add_menu_item("go-top", _("Bring to top"), "Home", None, z_order_menu)
        else:
            self._add_sub_menu_item(_("Z-order"), False)
            
        
        if len(self.__elements) == 1 and self.__elements[0].object.has_ufl_dialog:
            default = self._add_menu_item(None, _("Properties..."), None, self.__edit_properties)
        else:
            default = self._add_menu_item(None, _("Properties..."), None)
        
        self.setDefaultAction(default)
    
    def __hide(self, checked=False):
        command = HideElementsCommand(self.__diagram, self.__elements)
        
        Application().commands.execute(command)
    
    def __delete(self, checked=False):
        command = DeleteElementsCommand(tuple(element.object for element in self.__elements))
        
        Application().commands.execute(command)
    
    def __show_in_project(self, checked=False):
        Application().select_item(self.__elements[0].object)
    
    def __zorder_back(self, checked=False):
        pass
    
    def __zorder_forward(self, checked=False):
        pass
    
    def __zorder_bottom(self, checked=False):
        pass
    
    def __zorder_top(self, checked=False):
        pass
    
    def __edit_properties(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__elements[0].object)
