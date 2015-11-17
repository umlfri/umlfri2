from PySide.QtCore import Qt
from PySide.QtGui import QMainWindow, QTabWidget, QDockWidget

from umlfri2.application import Application
from .propertieswidget import PropertiesWidget
from .toolbox import ToolBox
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
        
        self.__toolbox_dock = QDockWidget()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.__toolbox_dock)
        self.__toolbox = ToolBox()
        self.__toolbox_dock.setWidget(self.__toolbox)
        
        self.__project_dock = QDockWidget()
        self.addDockWidget(Qt.RightDockWidgetArea, self.__project_dock)
        self.__project_tree = ProjectTree()
        self.__project_tree.reload()
        self.__project_dock.setWidget(self.__project_tree)
        
        self.__properties_dock = QDockWidget()
        self.addDockWidget(Qt.RightDockWidgetArea, self.__properties_dock)
        self.__properties = PropertiesWidget()
        self.__properties_dock.setWidget(self.__properties)
        
        self.__reopen_diagrams()
        self.reload_texts()
    
    def __tab_changed(self, index):
        Application().tabs.select_tab(self.__tabs.widget(index).diagram)
    
    def __reopen_diagrams(self):
        for tab in Application().tabs:
            self.__tabs.addTab(CanvasWidget(self, tab.drawing_area), image_loader.load_icon(tab.icon), tab.name)
    
    def reload_texts(self):
        self.setWindowTitle(_("UML .FRI 2"))
        
        self.__toolbox_dock.setWindowTitle(_("Tools"))
        self.__project_dock.setWindowTitle(_("Project"))
        self.__properties_dock.setWindowTitle(_("Properties"))
        
        self.__toolbox.reload_texts()
        self.__project_tree.reload_texts()
        self.__properties.reload_texts()
