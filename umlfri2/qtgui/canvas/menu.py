from PySide.QtGui import QMenu, QAction, QKeySequence, QIcon

from umlfri2.application import Application
from umlfri2.application.commands.diagram import HideConnectionCommand, HideElementsCommand
from umlfri2.application.commands.model import DeleteConnectionCommand, DeleteElementsCommand, ReverseConnectionCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT
from umlfri2.model.connection import ConnectionVisual
from umlfri2.qtgui.properties import PropertiesDialog


class CanvasContextMenu(QMenu):
    def __init__(self, main_window, drawing_area):
        super().__init__()
        
        self.__main_window = main_window
        self.__drawing_area = drawing_area
        self.__selected = tuple(self.__drawing_area.selection.selected_visuals)
        
        if len(self.__selected) > 1:
            self.__selected_object = None
        elif self.__selected:
            self.__selected_object = self.__selected[0].object
        else:
            self.__selected_object = self.__drawing_area.diagram
        
        diagram = drawing_area.selection.is_diagram_selected
        connection = drawing_area.selection.is_connection_selected
        
        self.__add_menu_item(None, _("Hide"), QKeySequence.Delete, not diagram, self.__hide_selection)
        self.__add_menu_item("edit-delete", _("Delete"), DELETE_FROM_PROJECT, not diagram, self.__delete_selection)
        self.addSeparator()
        self.__add_menu_item(None, _("Reverse connection"), None, connection, self.__reverse_connection)
        default = self.__add_menu_item(None, _("Properties..."), None,
                                       self.__selected_object and self.__selected_object.has_ufl_dialog,
                                       self.__edit_properties)
        
        if not diagram:
            self.setDefaultAction(default)

    def __add_menu_item(self, icon, label, shortcut, enabled=True, action=None):
        ret = QAction(label, self)
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        if action is not None:
            ret.triggered.connect(action)
        if not enabled:
            ret.setEnabled(False)
        self.addAction(ret)
        return ret
    
    def __hide_selection(self, checked=False):
        if isinstance(self.__selected[0], ConnectionVisual):
            command = HideConnectionCommand(self.__drawing_area.diagram, self.__selected[0])
        else:
            command = HideElementsCommand(self.__drawing_area.diagram, self.__selected)
        
        Application().commands.execute(command)
    
    def __delete_selection(self, checked=False):
        if isinstance(self.__selected[0], ConnectionVisual):
            command = DeleteConnectionCommand(self.__selected[0].object)
        else:
            command = DeleteElementsCommand(tuple(element.object for element in self.__selected))
        
        Application().commands.execute(command)
    
    def __reverse_connection(self, checked=False):
        command = ReverseConnectionCommand(self.__selected_object)
        
        Application().commands.execute(command)
    
    def __edit_properties(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__selected_object)
