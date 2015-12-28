from functools import partial

from PySide.QtGui import QMenu

from umlfri2.application import Application
from umlfri2.qtgui.properties import PropertiesDialog


class ProjectTreeDiagramMenu(QMenu):
    def __init__(self, main_window, diagram): 
        super().__init__()
        
        self.__main_window = main_window
        
        show = self.addAction(_("Show diagram in tab"))
        show.triggered.connect(partial(self.__show_diagram_action, diagram))
        self.setDefaultAction(show)
        
        self.addSeparator()
        self.addAction(_("Properties...")).triggered.connect(partial(self.__open_properties_action, diagram))
    
    def __show_diagram_action(self, diagram, checked=False):
        Application().tabs.select_tab(diagram)
    
    def __open_properties_action(self, object, checked=False):
        PropertiesDialog.open_for(self.__main_window, object)
