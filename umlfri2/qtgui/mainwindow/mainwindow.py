from PySide.QtCore import Qt
from PySide.QtGui import QMainWindow, QTabWidget, QDockWidget

from umlfri2.application import Application
from .projecttree import ProjectTree
from ..canvas import CanvasWidget


class UmlFriMainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.__tabs = QTabWidget()
        self.__tabs.setTabsClosable(True)
        self.setCentralWidget(self.__tabs)
        self.__reopen_diagrams()
        
        self.__tabs.setFocusPolicy(Qt.NoFocus)
        
        self.__toolbox_dock = QDockWidget("Tools")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.__toolbox_dock)
        
        self.__project_dock = QDockWidget("Project")
        self.addDockWidget(Qt.RightDockWidgetArea, self.__project_dock)
        self.__project_tree = ProjectTree()
        self.__project_tree.reload()
        self.__project_dock.setWidget(self.__project_tree)
        
        self.__properties_dock = QDockWidget("Properties")
        self.addDockWidget(Qt.RightDockWidgetArea, self.__properties_dock)
    
    def __reopen_diagrams(self):
        for tab in Application().tabs:
            self.__tabs.addTab(CanvasWidget(tab), tab.name)
