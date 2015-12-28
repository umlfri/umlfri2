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
        self.__diagram = diagram
        
        show = self.addAction(_("Show diagram"))
        show.triggered.connect(self.__show_diagram_action)
        self.setDefaultAction(show)
        
        action = self.addAction(_("Delete"))
        action.setIcon(QIcon.fromTheme("edit-delete"))
        action.setShortcut(QKeySequence(DELETE_FROM_PROJECT))
        action.triggered.connect(self.__delete_diagram_action)
        
        self.addSeparator()
        self.addAction(_("Properties...")).triggered.connect(self.__open_properties_action)
    
    def __show_diagram_action(self, checked=False):
        Application().tabs.select_tab(self.__diagram)
    
    def __delete_diagram_action(self, checked=False):
        command = DeleteDiagramCommand(self.__diagram)
        Application().commands.execute(command)
    
    def __open_properties_action(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__diagram)
