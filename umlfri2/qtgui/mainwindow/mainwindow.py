import os.path

from PySide.QtCore import Qt, QSettings
from PySide.QtGui import QMainWindow, QTabWidget, QDockWidget, QMessageBox, QFileDialog, QIcon, QTabBar

from umlfri2.application import Application
from umlfri2.application.addon import AddOnState
from umlfri2.application.events.addon import PluginStateChangedEvent
from umlfri2.application.events.application import LanguageChangedEvent, ChangeStatusChangedEvent
from umlfri2.application.events.model import ObjectDataChangedEvent
from umlfri2.application.events.solution import OpenSolutionEvent, SaveSolutionEvent
from umlfri2.application.events.tabs import OpenTabEvent, ChangedCurrentTabEvent, ClosedTabEvent
from umlfri2.constants.paths import GRAPHICS, CONFIG
from umlfri2.model import Diagram
from umlfri2.qtgui.base.clipboard import QtClipboardAdatper
from umlfri2.qtgui.newproject import NewProjectDialog
from umlfri2.qtgui.startpage import StartPage
from .addontoolbar import AddOnToolBar
from .aligntoolbar import AlignToolBar
from .menu import MainWindowMenu
from .toolbar import MainToolBar
from ..base import image_loader
from ..canvas import ScrolledCanvasWidget, CanvasWidget
from ..projecttree import ProjectTree
from ..properties import PropertiesWidget
from ..toolbox import MainToolBox


class UmlFriMainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(GRAPHICS, "icon", "icon.ico")))
        self.__tabs = QTabWidget()
        self.__tabs.setTabsClosable(True)
        self.setCentralWidget(self.__tabs)
        
        self.__tabs.setMovable(True)
        self.__tabs.setFocusPolicy(Qt.NoFocus)
        self.__tabs.setDocumentMode(True)
        self.__tabs.currentChanged.connect(self.__tab_changed)
        self.__tabs.tabCloseRequested.connect(self.__tab_close_requested)
        
        self.__toolbox_dock = QDockWidget()
        self.__toolbox_dock.setObjectName("tools")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.__toolbox_dock)
        self.__toolbox = MainToolBox()
        self.__toolbox_dock.setWidget(self.__toolbox)
        
        self.__project_dock = QDockWidget()
        self.__project_dock.setObjectName("project")
        self.addDockWidget(Qt.RightDockWidgetArea, self.__project_dock)
        self.__project_tree = ProjectTree(self)
        self.__project_tree.reload()
        self.__project_dock.setWidget(self.__project_tree)
        
        self.__properties_dock = QDockWidget()
        self.__properties_dock.setObjectName("tools")
        self.addDockWidget(Qt.RightDockWidgetArea, self.__properties_dock)
        self.__properties = PropertiesWidget(self)
        self.__properties_dock.setWidget(self.__properties)
        
        self.__tool_bar = MainToolBar(self)
        self.__tool_bar.setObjectName("toolbar")
        self.addToolBar(self.__tool_bar)
        
        self.__align_tool_bar = AlignToolBar()
        self.__align_tool_bar.setObjectName("alignment")
        self.addToolBar(self.__align_tool_bar)
        
        self.__addon_toolbars = []
        self.__create_addon_toolbars()
        
        self.__menu_bar = MainWindowMenu(self)
        self.setMenuBar(self.__menu_bar)
        
        self.setUnifiedTitleAndToolBarOnMac(True)
        
        self.__clipboard_adapter = QtClipboardAdatper()
        
        self.__ignore_change_tab = False
        
        Application().event_dispatcher.subscribe(OpenTabEvent, self.__open_tab)
        Application().event_dispatcher.subscribe(ChangedCurrentTabEvent, self.__change_tab)
        Application().event_dispatcher.subscribe(ClosedTabEvent, self.__close_tab)
        Application().event_dispatcher.subscribe(ObjectDataChangedEvent, self.__object_changed)
        Application().event_dispatcher.subscribe(OpenSolutionEvent, self.__solution_file_changed)
        Application().event_dispatcher.subscribe(SaveSolutionEvent, self.__solution_file_changed)
        Application().event_dispatcher.subscribe(ChangeStatusChangedEvent, self.__change_status_changed)
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        Application().event_dispatcher.subscribe(PluginStateChangedEvent, self.__plugin_state_changed)
        
        self.__reload_texts()
        
        self.__handle_last_tab()
        
        self.__restore_window_state()
    
    def __handle_last_tab(self):
        if self.__tabs.count() == 0:
            self.__tabs.addTab(StartPage(self), _("Start Page"))
        
        if self.__tabs.count() == 1 and isinstance(self.__tabs.widget(0), StartPage):
            tab_close_enabled = False
        else:
            tab_close_enabled = True
        
        for no in range(self.__tabs.count()):
            self.__tabs.tabBar().tabButton(no, QTabBar.RightSide).setEnabled(tab_close_enabled)
    
    def __tab_changed(self, index):
        if self.__ignore_change_tab:
            return
        
        if index >= 0:
            widget = self.__tabs.widget(index)
            
            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget)):
                Application().tabs.select_tab(widget.diagram)
            else:
                Application().tabs.select_tab(None)
    
    def __tab_close_requested(self, index):
        widget = self.__tabs.widget(index)
        if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget)):
            Application().tabs.close_tab(widget.diagram)
        elif isinstance(widget, StartPage):
            self.__tabs.removeTab(self.__tabs.indexOf(widget))
            self.__handle_last_tab()
    
    def __open_tab(self, event):
        canvas = ScrolledCanvasWidget(self, event.tab.drawing_area)
        self.__tabs.addTab(canvas, image_loader.load_icon(event.tab.icon), event.tab.name)
        self.__handle_last_tab()
    
    def __change_tab(self, event):
        if event.tab is None:
            return
        
        for widget_id in range(self.__tabs.count()):
            widget = self.__tabs.widget(widget_id)
            
            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget))\
                    and widget.diagram is event.tab.drawing_area.diagram:
                self.__tabs.setCurrentWidget(widget)
                return
    
    def __close_tab(self, event):
        for widget_id in range(self.__tabs.count()):
            widget = self.__tabs.widget(widget_id)
            
            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget))\
                    and widget.diagram is event.tab.drawing_area.diagram:
                self.__ignore_change_tab = True
                try:
                    self.__tabs.removeTab(widget_id)
                finally:
                    self.__ignore_change_tab = False
                break
        self.__handle_last_tab()
    
    def __object_changed(self, event):
        if not isinstance(event.object, Diagram):
            return
        
        for widget_id in range(self.__tabs.count()):
            widget = self.__tabs.widget(widget_id)
            
            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget))\
                    and widget.diagram is event.object:
                self.__tabs.setTabText(widget_id, widget.diagram.get_display_name())
                return
    
    def __change_status_changed(self, event):
        self.__reload_window_title()
    
    def __solution_file_changed(self, event):
        self.__reload_window_title()
    
    def createPopupMenu(self):
        return None
    
    def closeEvent(self, event):
        if self.__check_save(_("Application Exit")):
            self.__save_window_state()
            event.accept()
        else:
            event.ignore()
    
    def __save_window_state(self):
        settings = QSettings(os.path.join(CONFIG, 'qt.ini'), QSettings.IniFormat)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())
    
    def __restore_window_state(self):
        settings = QSettings(os.path.join(CONFIG, 'qt.ini'), QSettings.IniFormat)
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("window_state"))

    def __check_save(self, title):
        if Application().unsaved:
            message_box = QMessageBox(self)
            message_box.setIcon(QMessageBox.Question)
            message_box.setWindowTitle(title)
            message_box.setText(_("The model has been modified."))
            message_box.setInformativeText(_("Do you want to save the project?"))
            message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            message_box.setDefaultButton(QMessageBox.Save)
            message_box.button(QMessageBox.Save).setText(_("Save"))
            message_box.button(QMessageBox.Discard).setText(_("Close without saving"))
            message_box.button(QMessageBox.Cancel).setText(_("Cancel"))
            resp = message_box.exec_()
            
            if resp == QMessageBox.Cancel:
                return False
            elif resp == QMessageBox.Save:
                return self.save_solution()
        return True
    
    def get_toolbar_actions(self):
        yield self.__tool_bar.toggleViewAction()
        yield self.__align_tool_bar.toggleViewAction()
        
        for toolbar in self.__addon_toolbars:
            yield toolbar.toggleViewAction()
    
    def get_dock_actions(self):
        yield self.__toolbox_dock.toggleViewAction()
        yield self.__project_dock.toggleViewAction()
        yield self.__properties_dock.toggleViewAction()
    
    @property
    def project_tree(self):
        return self.__project_tree
    
    def new_project(self):
        dialog = NewProjectDialog.open_dialog(self)
        if dialog:
            if dialog.new_solution and Application().unsaved:
                if not self.__check_save(_("New Project")):
                    return
            Application().new_project(dialog.selected_template, dialog.new_solution, dialog.project_name)
    
    def open_solution(self):
        file_name, filter = QFileDialog.getOpenFileName(
            self,
            caption=_("Open Project"),
            filter=_("UML .FRI 2 projects") + "(*.frip2)"
        )
        if file_name:
            self.open_solution_from_file(file_name)

    def open_solution_from_file(self, file_name):
        if self.__check_save(_("Open Project")):
            Application().open_solution(file_name)

    def save_solution(self):
        if Application().should_save_as:
            return self.save_solution_as()
        else:
            Application().save_solution()
            return True
    
    def save_solution_as(self):
        file_name, filter = QFileDialog.getSaveFileName(
            self,
            caption=_("Save Project"),
            filter=_("UML .FRI 2 projects") + "(*.frip2)"
        )
        if file_name:
            if '.' not in os.path.basename(file_name):
                file_name = file_name + '.frip2'
            Application().save_solution_as(file_name)
            return True # the project was saved
        else:
            return False # the project was not saved
    
    def __create_addon_toolbars(self):
        for addon in Application().addons:
            self.__create_toolbars_for(addon)

    def __plugin_state_changed(self, event):
        if event.addon_state == AddOnState.started:
            self.__create_toolbars_for(event.addon)
        elif event.addon_state == AddOnState.stopped:
            self.__remove_toolbars_for(event.addon)

    def __create_toolbars_for(self, addon):
        if addon.state != AddOnState.started:
            return
        
        for toolbar in addon.gui_injection.toolbars:
            qt_toolbar = AddOnToolBar(toolbar)
            qt_toolbar.setObjectName(toolbar.label)
            self.addToolBar(qt_toolbar)
            self.__addon_toolbars.append(qt_toolbar)

    def __remove_toolbars_for(self, addon):
        if addon.state != AddOnState.stopped:
            return
        
        for toolbar in self.__addon_toolbars[:]:
            if toolbar.toolbar.addon is addon:
                self.removeToolBar(toolbar)
                toolbar.deleteLater()
                self.__addon_toolbars.remove(toolbar)

    def __reload_window_title(self):
        title = _("UML .FRI 2")
        if Application().solution_name is not None:
            title += " [{0}]".format(Application().solution_name)
        elif Application().solution is not None:
            title += " [{0}]".format(_("unsaved"))
        
        if Application().commands.changed:
            title += "*"
        
        self.setWindowTitle(title)
    
    def __reload_texts(self):
        self.__reload_window_title()
        
        self.__toolbox_dock.setWindowTitle(_("Tools"))
        self.__project_dock.setWindowTitle(_("Project"))
        self.__properties_dock.setWindowTitle(_("Properties"))
