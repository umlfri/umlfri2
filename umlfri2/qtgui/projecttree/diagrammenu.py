from functools import partial

from PySide.QtGui import QMenu, QIcon, QKeySequence

from umlfri2.application import Application
from umlfri2.application.commands.model import DeleteDiagramCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT
from umlfri2.qtgui.properties import PropertiesDialog


class ProjectTreeDiagramMenu(QMenu):
    def __init__(self, main_window, diagram): 
        super().__init__()
        
        self.__main_window = main_window
        
        show = self.addAction(_("Show diagram in tab"))
        show.triggered.connect(partial(self.__show_diagram_action, diagram))
        self.setDefaultAction(show)
        
        self.addSeparator()
        action = self.addAction(_("Delete"))
        action.setIcon(QIcon.fromTheme("edit-delete"))
        action.setShortcut(QKeySequence(DELETE_FROM_PROJECT))
        action.triggered.connect(partial(self.__delete_diagram_action, diagram))
        
        self.addSeparator()
        self.addAction(_("Properties...")).triggered.connect(partial(self.__open_properties_action, diagram))
    
    def __show_diagram_action(self, diagram, checked=False):
        Application().tabs.select_tab(diagram)
    
    def __delete_diagram_action(self, diagram, checked=False):
        command = DeleteDiagramCommand(diagram)
        Application().commands.execute(command)
    
    def __open_properties_action(self, object, checked=False):
        PropertiesDialog.open_for(self.__main_window, object)
