import os.path

from PySide.QtCore import Qt
from PySide.QtGui import QMainWindow, QTabWidget, QDockWidget, QMessageBox, QFileDialog, QIcon
from umlfri2.application import Application
from umlfri2.application.events.model import ObjectChangedEvent
from umlfri2.application.events.solution import OpenSolutionEvent, SaveSolutionEvent
from umlfri2.application.events.tabs import OpenTabEvent, ChangedCurrentTabEvent, ClosedTabEvent
from umlfri2.model import Diagram
from umlfri2.paths import GRAPHICS
from .menu import MainWindowMenu
from .propertieswidget import PropertiesWidget
from .toolbox import ToolBox
from ..base import image_loader
from .projecttree import ProjectTree
from ..canvas import CanvasWidget


class UmlFriMainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(GRAPHICS, "icon", "icon.ico")))
        self.__tabs = QTabWidget()
        self.__tabs.setTabsClosable(True)
        self.setCentralWidget(self.__tabs)
        
        self.__tabs.setMovable(True)
        self.__tabs.setFocusPolicy(Qt.NoFocus)
        self.__tabs.currentChanged.connect(self.__tab_changed)
        self.__tabs.tabCloseRequested.connect(self.__tab_close_requested)
        
        self.__toolbox_dock = QDockWidget()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.__toolbox_dock)
        self.__toolbox = ToolBox()
        self.__toolbox_dock.setWidget(self.__toolbox)
        
        self.__project_dock = QDockWidget()
        self.addDockWidget(Qt.RightDockWidgetArea, self.__project_dock)
        self.__project_tree = ProjectTree(self)
        self.__project_tree.reload()
        self.__project_dock.setWidget(self.__project_tree)
        
        self.__properties_dock = QDockWidget()
        self.addDockWidget(Qt.RightDockWidgetArea, self.__properties_dock)
        self.__properties = PropertiesWidget()
        self.__properties_dock.setWidget(self.__properties)
        
        self.__menu_bar = MainWindowMenu(self)
        self.setMenuBar(self.__menu_bar)
        
        self.reload_texts()
        
        Application().event_dispatcher.register(OpenTabEvent, self.__open_tab)
        Application().event_dispatcher.register(ChangedCurrentTabEvent, self.__change_tab)
        Application().event_dispatcher.register(ClosedTabEvent, self.__close_tab)
        Application().event_dispatcher.register(ObjectChangedEvent, self.__object_changed)
        Application().event_dispatcher.register(OpenSolutionEvent, self.__solution_name_changed)
        Application().event_dispatcher.register(SaveSolutionEvent, self.__solution_name_changed)
    
    def __tab_changed(self, index):
        if index >= 0:
            Application().tabs.select_tab(self.__tabs.widget(index).diagram)
    
    def __tab_close_requested(self, index):
        Application().tabs.close_tab(self.__tabs.widget(index).diagram)
    
    def __open_tab(self, event):
        self.__tabs.addTab(CanvasWidget(self, event.tab.drawing_area), image_loader.load_icon(event.tab.icon),
                           event.tab.name)
    
    def __change_tab(self, event):
        for widget_id in range(self.__tabs.count()):
            widget = self.__tabs.widget(widget_id)
            
            if widget.diagram is event.tab.drawing_area.diagram:
                self.__tabs.setCurrentWidget(widget)
                return
    
    def __close_tab(self, event):
        for widget_id in range(self.__tabs.count()):
            widget = self.__tabs.widget(widget_id)
            
            if widget.diagram is event.tab.drawing_area.diagram:
                self.__tabs.removeTab(widget_id)
                return
    
    def __object_changed(self, event):
        if not isinstance(event.object, Diagram):
            return
        
        for widget_id in range(self.__tabs.count()):
            widget = self.__tabs.widget(widget_id)
            
            if widget.diagram is event.object:
                self.__tabs.setTabText(widget_id, widget.diagram.get_display_name())
                return
    
    def __solution_name_changed(self, event):
        self.__reload_window_title()
    
    def createPopupMenu(self):
        return None
    
    def closeEvent(self, event):
        if self.check_save():
            event.accept()
        else:
            event.ignore()

    def check_save(self):
        if Application().unsaved:
            resp = QMessageBox.question(self, _("Application exit"), _("Do you want to save the project?"),
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                        QMessageBox.Yes)

            if resp == QMessageBox.Cancel:
                return False
            elif resp == QMessageBox.Yes:
                return self.save_solution()
        return True

    def get_dock_actions(self):
        yield self.__toolbox_dock.toggleViewAction()
        yield self.__project_dock.toggleViewAction()
        yield self.__properties_dock.toggleViewAction()
    
    def open_solution(self):
        file_name, filter = QFileDialog.getOpenFileName(self, filter = _("UML .FRI 2 projects") + "(*.frip2)")
        if file_name:
            Application().open_solution(file_name)
    
    def save_solution(self):
        if Application().should_save_as:
            return self.save_solution_as()
        else:
            Application().save_solution()
            return True
    
    def save_solution_as(self):
        file_name, filter = QFileDialog.getSaveFileName(self, filter = _("UML .FRI 2 projects") + "(*.frip2)")
        if file_name:
            if '.' not in os.path.basename(file_name):
                file_name = file_name + '.frip2'
            Application().save_solution_as(file_name)
            return True # the project was saved
        else:
            return False # the project was not saved
    
    def __reload_window_title(self):
        title = _("UML .FRI 2")
        if Application().solution_name is not None:
            title += " [{0}]".format(Application().solution_name)
        self.setWindowTitle(title)
    
    def reload_texts(self):
        self.__reload_window_title()
        
        self.__toolbox_dock.setWindowTitle(_("Tools"))
        self.__project_dock.setWindowTitle(_("Project"))
        self.__properties_dock.setWindowTitle(_("Properties"))
        
        self.__toolbox.reload_texts()
        self.__project_tree.reload_texts()
        self.__properties.reload_texts()
        
        self.__menu_bar.reload_texts()
