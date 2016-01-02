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
        
        self._add_menu_item(None, _("Hide"), QKeySequence.Delete, self.__hide)
        self._add_menu_item("edit-delete", _("Delete"), DELETE_FROM_PROJECT, self.__delete)
        
        self.addSeparator()
        
        if len(self.__elements) == 1:
            self._add_menu_item(None, _("Find in the project tree"), None, self.__show_in_project)
        else:
            self._add_menu_item(None, _("Find in the project tree"), None)
        
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
        self.__main_window.project_tree.select(self.__elements[0].object)
    
    def __edit_properties(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__elements[0].object)
