from ..base.contextmenu import ContextMenu
from ..properties import PropertiesDialog


class CanvasDiagramMenu(ContextMenu):
    def __init__(self, main_window, drawing_area, diagram):
        super().__init__()
        
        self.__main_window = main_window
        self.__diagram = diagram
        
        if self.__diagram.has_ufl_dialog:
            self._add_menu_item(None, _("Properties..."), None, self.__edit_properties)
        else:
            self._add_menu_item(None, _("Properties..."), None)
    
    def __edit_properties(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__diagram)
