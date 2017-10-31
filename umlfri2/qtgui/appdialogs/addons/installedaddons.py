from collections import namedtuple
from functools import partial

from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QPushButton, QMenu
from umlfri2.application import Application
from umlfri2.application.addon import AddOnState
from umlfri2.application.events.addon import AddonStateChangedEvent
from .listwidget import AddOnListWidget
from .info import AddOnInfoDialog


class InstalledAddOnList(AddOnListWidget):
    __AddonButtons = namedtuple('AddonButtons', ['start', 'stop'])
    
    def __init__(self):
        super().__init__()

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__timer_event)
        
        Application().event_dispatcher.subscribe(AddonStateChangedEvent, self.__addon_state_changed)
    
    @property
    def _addons(self):
        return Application().addons
    
    def _addon_content_menu(self, addon):
        menu = QMenu(self)
        
        if addon.state != AddOnState.none:
            start = menu.addAction(QIcon.fromTheme("media-playback-start"), _("Start"))
            stop = menu.addAction(QIcon.fromTheme("media-playback-stop"), _("Stop"))
            
            start.triggered.connect(partial(self.__start_addon, addon))
            stop.triggered.connect(partial(self.__stop_addon, addon))
            
            if addon.state == AddOnState.started:
                start.setEnabled(False)
            
            if addon.state in (AddOnState.stopped, AddOnState.error):
                stop.setEnabled(False)
            
            menu.addSeparator()
        
        if addon.homepage:
            homepage = menu.addAction(QIcon.fromTheme("application-internet"), _("Homepage"))
            homepage.triggered.connect(partial(self.__show_homepage, addon))
        about = menu.addAction(QIcon.fromTheme("help-about"), _("About..."))
        about.triggered.connect(partial(self.__show_info, addon))
        
        menu.addSeparator()
        
        if not addon.is_system_addon:
            menu.addAction(QIcon.fromTheme("edit-delete"), _("Uninstall"))
        
        return menu
    
    def _addon_button_factory(self):
        self.__addon_buttons = {}
        return self
    
    def add_buttons(self, addon, button_box):
        if addon.state != AddOnState.none:
            start_button = QPushButton(QIcon.fromTheme("media-playback-start"), _("Start"))
            start_button.setFocusPolicy(Qt.NoFocus)
            start_button.setEnabled(addon.state in (AddOnState.stopped, AddOnState.error))
            start_button.clicked.connect(partial(self.__start_addon, addon))
            button_box.addWidget(start_button)

            stop_button = QPushButton(QIcon.fromTheme("media-playback-stop"), _("Stop"))
            stop_button.setFocusPolicy(Qt.NoFocus)
            stop_button.setEnabled(addon.state == AddOnState.started)
            stop_button.clicked.connect(partial(self.__stop_addon, addon))
            button_box.addWidget(stop_button)

            self.__addon_buttons[addon.identifier] = self.__AddonButtons(start_button, stop_button)
    
    def __show_info(self, addon, checked=False):
        dialog = AddOnInfoDialog(self, addon)
        dialog.exec_()
    
    def __show_homepage(self, addon, checked=False):
        QDesktopServices.openUrl(QUrl(addon.homepage))
    
    def __start_addon(self, addon, checked=False):
        self.__run_process(addon.start())
    
    def __stop_addon(self, addon, checked=False):
        self.__run_process(addon.stop())
    
    def __run_process(self, starter_stopper):
        self.__starter_stopper = starter_stopper
        self.__timer.start(100)
        self.__timer_event()
        self.setEnabled(False)
    
    def __timer_event(self):
        if self.__starter_stopper.finished:
            self.__timer.stop()
            self.setEnabled(True)
        else:
            self.__starter_stopper.do()
    
    def __addon_state_changed(self, event):
        if event.addon.identifier in self.__addon_buttons:
            buttons = self.__addon_buttons[event.addon.identifier]
            buttons.start.setEnabled(event.addon.state in (AddOnState.stopped, AddOnState.error))
            buttons.stop.setEnabled(event.addon.state == AddOnState.started)
