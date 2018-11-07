import os.path

from PyQt5.QtCore import Qt, QSettings, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QMessageBox, QFileDialog, QApplication

from umlfri2.application import Application
from umlfri2.application.addon.local import AddOnState
from umlfri2.application.events.addon import AddOnStateChangedEvent
from umlfri2.application.events.application import LanguageChangedEvent, ChangeStatusChangedEvent, \
    UpdateCheckFinishedEvent
from umlfri2.application.events.solution import OpenSolutionEvent, SaveSolutionEvent, CloseSolutionEvent
from umlfri2.application.events.tabs import TabLockStatusChangedEvent
from umlfri2.constants.paths import GRAPHICS, CONFIG
from umlfri2.constants.solutionfile import SOLUTION_EXTENSION
from ..base.clipboard import QtClipboardAdatper
from ..newproject import NewProjectDialog
from ..splashscreen.exitscreen import ExitScreen
from .addontoolbar import AddOnToolBar
from .aligntoolbar import AlignToolBar
from .menu import MainWindowMenu
from .toolbar import MainToolBar
from ..projecttree import ProjectTree
from ..properties import PropertiesWidget
from ..toolbox import MainToolBox
from .tabs import Tabs


class UmlFriMainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(GRAPHICS, "icon", "icon.ico")))
        self.__tabs = Tabs(self)
        self.setCentralWidget(self.__tabs)

        self.__toolbox_dock = QDockWidget()
        self.__toolbox_dock.setObjectName("tools")
        self.__toolbox_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.__toolbox_dock)
        self.__toolbox = MainToolBox(self.__toolbox_dock)
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
        
        self.setAcceptDrops(True)
        
        self.__clipboard_adapter = QtClipboardAdatper()
        
        Application().event_dispatcher.subscribe(CloseSolutionEvent, self.__solution_file_changed)
        Application().event_dispatcher.subscribe(OpenSolutionEvent, self.__solution_file_changed)
        Application().event_dispatcher.subscribe(SaveSolutionEvent, self.__solution_file_changed)
        Application().event_dispatcher.subscribe(ChangeStatusChangedEvent, self.__change_status_changed)
        Application().event_dispatcher.subscribe(TabLockStatusChangedEvent, self.__tab_lock_status_changed)
        Application().event_dispatcher.subscribe(LanguageChangedEvent, self.__language_changed)
        Application().event_dispatcher.subscribe(AddOnStateChangedEvent, self.__plugin_state_changed)
        Application().event_dispatcher.subscribe(UpdateCheckFinishedEvent, self.__update_check)
        
        self.__reload_texts()
        
        self.__restore_window_state()

        if not Application().about.updates.checking_update:
            self.__update_dialog()
    
    def __language_changed(self, event):
        self.__reload_texts()
    
    def __change_status_changed(self, event):
        self.__reload_window_title()
    
    def __tab_lock_status_changed(self, event):
        self.__reload_window_title()
    
    def __solution_file_changed(self, event):
        self.__reload_window_title()
    
    def createPopupMenu(self):
        return None
    
    def closeEvent(self, event):
        if self.__check_save(_("Application Exit")):
            self.__save_window_state()
            #event.accept()
            exit_screen = ExitScreen()
            self.setEnabled(False)
            exit_screen.start()
        event.ignore()
    
    def dragEnterEvent(self, event):
        if len(event.mimeData().urls()) == 1 and event.mimeData().urls()[0].isLocalFile():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        file = event.mimeData().urls()[0].toLocalFile()
        self.open_solution_from_file(file)
    
    def __save_window_state(self):
        settings = QSettings(os.path.join(CONFIG, 'qt.ini'), QSettings.IniFormat)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())
        settings.setValue("toolbox_expanded", self.__toolbox.expanded)
    
    def __restore_window_state(self):
        settings = QSettings(os.path.join(CONFIG, 'qt.ini'), QSettings.IniFormat)
        if settings.contains("geometry"):
            self.restoreGeometry(settings.value("geometry"))
        if settings.contains("window_state"):
            self.restoreState(settings.value("window_state"))
        if settings.contains("toolbox_expanded"):
            self.__toolbox.expanded = settings.value("toolbox_expanded", type=bool)

    def __check_save(self, title):
        if Application().unsaved:
            message_box = QMessageBox(self)
            message_box.setWindowModality(Qt.WindowModal)
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
            filter=_("UML .FRI 2 projects") + "(*.{0})".format(SOLUTION_EXTENSION)
        )
        if file_name:
            self.open_solution_from_file(file_name)

    def open_recent_file(self, recent_file):
        if not recent_file.exists:
            message_box = QMessageBox(self)
            message_box.setWindowModality(Qt.WindowModal)
            message_box.setIcon(QMessageBox.Question)
            message_box.setWindowTitle(_("Missing file"))
            message_box.setText(_("The requested file '{0}' missing.").format(recent_file.file_name))
            message_box.setInformativeText(_("Do you want to remove it from list?"))
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.Yes)
            message_box.button(QMessageBox.Yes).setText(_("Yes"))
            message_box.button(QMessageBox.No).setText(_("No"))
            resp = message_box.exec_()
            
            if resp == QMessageBox.Yes:
                recent_file.remove()
                pass
            
            return

        if self.__check_save(_("Open Project")):
            recent_file.open()

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
            filter=_("UML .FRI 2 projects") + "(*.{0})".format(SOLUTION_EXTENSION)
        )
        if file_name:
            if '.' not in os.path.basename(file_name):
                file_name = '{0}.{1}'.format(file_name, SOLUTION_EXTENSION)
            Application().save_solution_as(file_name)
            return True # the project was saved
        else:
            return False # the project was not saved
    
    def __create_addon_toolbars(self):
        for addon in Application().addons.local:
            self.__create_toolbars_for(addon)

    def __plugin_state_changed(self, event):
        if event.addon_state == AddOnState.started:
            self.__create_toolbars_for(event.addon)
        elif event.addon_state == AddOnState.stopped:
            self.__remove_toolbars_for(event.addon)

    def __create_toolbars_for(self, addon):
        if addon.state != AddOnState.started:
            return
        
        if addon.gui_injection is None:
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
    
    def __update_check(self, event):
        self.__update_dialog()
    
    def __update_dialog(self):
        latest_update = Application().about.updates.latest_version
        
        if latest_update is None:
            return
        
        if not latest_update.is_newer:
            return
        
        if latest_update.is_ignored:
            return
        
        current_window = QApplication.instance().activeWindow()
        
        if current_window.isModal():
            msg_parent = current_window
        else:
            msg_parent = self
        
        new_update = QMessageBox(msg_parent)
        new_update.setIcon(QMessageBox.Information)
        new_update.setWindowModality(Qt.WindowModal)
        new_update.setWindowTitle(_("New update"))
        new_update.setText(_("Application UML .FRI was updated to version '{0}' on the server.").format(latest_update.version))
        
        download = new_update.addButton(_("Download"), QMessageBox.ActionRole)
        ignore = new_update.addButton(_("Ignore This Update"), QMessageBox.ActionRole)
        remind_later = new_update.addButton(_("Remind me later"), QMessageBox.ActionRole)
        
        new_update.setDefaultButton(remind_later)
        new_update.setEscapeButton(remind_later)
        
        new_update.exec_()
        
        if new_update.clickedButton() is download:
            QDesktopServices.openUrl(QUrl(latest_update.url))
        elif new_update.clickedButton() is ignore:
            latest_update.ignore_update()
    
    def __reload_window_title(self):
        title = _("UML .FRI 2")
        if Application().solution_name is not None:
            title += " [{0}]".format(Application().solution_name)
        elif Application().solution is not None:
            title += " [{0}]".format(_("unsaved"))
        
        if Application().change_status:
            title += "*"
        
        self.setWindowTitle(title)
    
    def __reload_texts(self):
        self.__reload_window_title()
        
        self.__toolbox_dock.setWindowTitle(_("Tools"))
        self.__project_dock.setWindowTitle(_("Project"))
        self.__properties_dock.setWindowTitle(_("Properties"))
