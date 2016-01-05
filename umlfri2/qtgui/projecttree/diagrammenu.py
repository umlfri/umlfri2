from umlfri2.application import Application
from umlfri2.application.commands.model import DeleteDiagramCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT
from ..base.contextmenu import ContextMenu
from ..properties import PropertiesDialog


class ProjectTreeDiagramMenu(ContextMenu):
    def __init__(self, main_window, diagram): 
        super().__init__()
        
        self.__main_window = main_window
        self.__diagram = diagram
        
        show = self._add_menu_item(None, _("Show Diagram"), None, self.__show_diagram_action)
        self.setDefaultAction(show)
        
        self._add_menu_item("edit-delete", _("Delete"), DELETE_FROM_PROJECT, self.__delete_diagram_action)
        
        self.addSeparator()
        if self.__diagram.has_ufl_dialog:
            self._add_menu_item(None, _("Properties..."), None, self.__open_properties_action)
        else:
            self._add_menu_item(None, _("Properties..."), None)
    
    def __show_diagram_action(self, checked=False):
        Application().tabs.select_tab(self.__diagram)
    
    def __delete_diagram_action(self, checked=False):
        command = DeleteDiagramCommand(self.__diagram)
        Application().commands.execute(command)
    
    def __open_properties_action(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__diagram)
