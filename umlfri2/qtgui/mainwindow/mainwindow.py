from PySide.QtCore import Qt
from PySide.QtGui import QMainWindow, QTabWidget, QDockWidget

from umlfri2.application import Application
from umlfri2.qtgui.mainwindow.toolbox import ToolBox
from ..base import image_loader
from .projecttree import ProjectTree
from ..canvas import CanvasWidget


class UmlFriMainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.__tabs = QTabWidget()
        self.__tabs.setTabsClosable(True)
        self.setCentralWidget(self.__tabs)
        
        self.__tabs.setFocusPolicy(Qt.NoFocus)
        self.__tabs.currentChanged.connect(self.__tab_changed)
        
        self.__toolbox_dock = QDockWidget("Tools")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.__toolbox_dock)
        self.__toolbox = ToolBox()
        self.__toolbox_dock.setWidget(self.__toolbox)
        
        self.__project_dock = QDockWidget("Project")
        self.addDockWidget(Qt.RightDockWidgetArea, self.__project_dock)
        self.__project_tree = ProjectTree()
        self.__project_tree.reload()
        self.__project_dock.setWidget(self.__project_tree)
        
        self.__properties_dock = QDockWidget("Properties")
        self.addDockWidget(Qt.RightDockWidgetArea, self.__properties_dock)
        
        self.__toolbox.set_diagram_type(None)
        
        self.__reopen_diagrams()
    
    def __tab_changed(self, index):
        Application().tabs.current_tab = self.__tabs.widget(index).tab
    
    def __reopen_diagrams(self):
        for tab in Application().tabs:
            self.__tabs.addTab(CanvasWidget(tab), image_loader.load_icon(tab.icon), tab.name)
