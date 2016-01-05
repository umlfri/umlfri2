from PySide.QtGui import QKeySequence

from umlfri2.application import Application
from umlfri2.application.commands.diagram import HideConnectionCommand
from umlfri2.application.commands.model import DeleteConnectionCommand, ReverseConnectionCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT
from ..base.contextmenu import ContextMenu
from ..properties import PropertiesDialog


class CanvasConnectionMenu(ContextMenu):
    def __init__(self, main_window, drawing_area, connection):
        super().__init__()
        
        self.__main_window = main_window
        self.__connection = connection
        self.__diagram = drawing_area.diagram
        
        self._add_menu_item(None, _("Hide"), QKeySequence.Delete, self.__hide)
        self._add_menu_item("edit-delete", _("Delete"), DELETE_FROM_PROJECT, self.__delete)
        
        self.addSeparator()
        
        self._add_menu_item(None, _("Reverse Connection"), None, self.__reverse_connection)
        
        if connection.object.has_ufl_dialog:
            default = self._add_menu_item(None, _("Properties..."), None, self.__edit_properties)
        else:
            default = self._add_menu_item(None, _("Properties..."), None)
        
        self.setDefaultAction(default)
    
    def __hide(self, checked=False):
        command = HideConnectionCommand(self.__diagram, self.__connection)
        
        Application().commands.execute(command)
    
    def __delete(self, checked=False):
        command = DeleteConnectionCommand(self.__connection.object)
        
        Application().commands.execute(command)
    
    def __reverse_connection(self, checked=False):
        command = ReverseConnectionCommand(self.__connection.object)
        
        Application().commands.execute(command)
    
    def __edit_properties(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__connection.object)
