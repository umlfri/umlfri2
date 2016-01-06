from PySide.QtGui import QKeySequence

from umlfri2.constants.keys import PASTE_DUPLICATE
from ..base.contextmenu import ContextMenu
from ..properties import PropertiesDialog


class CanvasDiagramMenu(ContextMenu):
    def __init__(self, main_window, drawing_area, diagram):
        super().__init__()
        
        self.__main_window = main_window
        self.__diagram = diagram
        
        if drawing_area.can_paste_snippet:
            self._add_menu_item("edit-paste", _("Paste"), QKeySequence.Paste, self.__paste_action)
        else:
            self._add_menu_item("edit-paste", _("Paste"), QKeySequence.Paste)
        
        if drawing_area.can_paste_snippet_duplicate:
            self._add_menu_item("edit-paste", _("Paste Duplicate"), PASTE_DUPLICATE, self.__duplicate_action)
        else:
            self._add_menu_item("edit-paste", _("Paste Duplicate"), PASTE_DUPLICATE)
        
        self.addSeparator()
        
        if self.__diagram.has_ufl_dialog:
            self._add_menu_item(None, _("Properties..."), None, self.__edit_properties)
        else:
            self._add_menu_item(None, _("Properties..."), None)
    
    def __paste_action(self, checked=False):
        pass
    
    def __duplicate_action(self, checked=False):
        pass
    
    def __edit_properties(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__diagram)
