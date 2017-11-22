from functools import partial

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenu

from umlfri2.application import Application
from umlfri2.application.events.addon import AddOnInstalledEvent, AddOnUninstalledEvent
from umlfri2.qtgui.appdialogs.addons.info import AddOnInfoDialog
from .listwidget import AddOnListWidget


class UpdateAddOnList(AddOnListWidget):
    def __init__(self, processes):
        super().__init__(check_boxes=True, show_prev_version=True)
        
        self.__processes = processes
        
        Application().event_dispatcher.subscribe(AddOnInstalledEvent, self.__addon_list_changed)
        Application().event_dispatcher.subscribe(AddOnUninstalledEvent, self.__addon_list_changed)
        
    @property
    def _addons(self):
        yield from Application().addons.online.updated_addons
    
    def _addon_button_factory(self):
        pass
    
    def _addon_content_menu(self, addon):
        menu = QMenu(self)
        
        install = menu.addAction(QIcon.fromTheme("system-software-update"), _("Update"))
        install.triggered.connect(partial(self.__update, addon))
        
        menu.addSeparator()
        
        if addon.homepage:
            homepage = menu.addAction(QIcon.fromTheme("application-internet"), _("Homepage"))
            homepage.triggered.connect(partial(self.__show_homepage, addon))
        
        about = menu.addAction(QIcon.fromTheme("help-about"), _("About..."))
        about.triggered.connect(partial(self.__show_info, addon))
        
        return menu

    def __addon_list_changed(self, event):
        self.refresh()
    
    def __update(self, addon, checked=False):
        self.__processes.run_process(addon.latest_version.update())
    
    def __show_info(self, addon, checked=False):
        dialog = AddOnInfoDialog(self, addon)
        dialog.exec_()
    
    def __show_homepage(self, addon, checked=False):
        QDesktopServices.openUrl(QUrl(addon.homepage))


class UpdateAddOnTab(QWidget):
    def __init__(self, processes):
        super().__init__()
        
        self.__processes = processes
        
        self.__addon_list = UpdateAddOnList(self.__processes)
        self.__addon_list.check_changed.connect(self.__addon_check_changed)
        
        self.__update_button = QPushButton(QIcon.fromTheme("system-software-update"), _("Update"))
        self.__update_button.clicked.connect(self.__update)
        
        layout = QVBoxLayout()
        layout.addWidget(self.__addon_list)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.__update_button)
        button_layout.setAlignment(Qt.AlignRight)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.__update_button.setEnabled(any(self.__addon_list.checked_addons))
    
    def __addon_check_changed(self):
        self.__update_button.setEnabled(any(self.__addon_list.checked_addons))
    
    def __update(self, checked=False):
        process = None
        
        for addon in self.__addon_list.checked_addons:
            if process is None:
                process = addon.latest_version.update()
            else:
                process = process.combine_with(addon.latest_version.update())
        
        if process is not None:
            self.__processes.run_process(process)
