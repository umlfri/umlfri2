from collections import namedtuple
from functools import partial

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QPushButton, QLabel, QMenu

from umlfri2.application import Application
from umlfri2.application.events.addon import AddOnInstalledEvent
from .installdialog import InstallAddOnDialog
from .info import AddOnInfoDialog
from .listwidget import AddOnListWidget


class OnlineAddOnList(AddOnListWidget):
    __OnlineAddonButtons = namedtuple('AddonButtons', ['install', 'installed_info'])
    
    def __init__(self, processes):
        super().__init__()
        
        self.__processes = processes
        
        Application().event_dispatcher.subscribe(AddOnInstalledEvent, self.__addon_installed)
    
    def _addon_button_factory(self):
        self.__buttons = {}
        return self
    
    def _addon_content_menu(self, addon):
        menu = QMenu(self)
        
        install = menu.addAction(QIcon.fromTheme("list-add"), _("Install"))
        install.triggered.connect(partial(self.__install, addon))

        if addon.local_addon is not None:
            install.setEnabled(False)
        
        menu.addSeparator()
        
        if addon.homepage:
            homepage = menu.addAction(QIcon.fromTheme("application-internet"), _("Homepage"))
            homepage.triggered.connect(partial(self.__show_homepage, addon))
        about = menu.addAction(QIcon.fromTheme("help-about"), _("About..."))
        about.triggered.connect(partial(self.__show_info, addon))
        
        return menu
    
    def add_buttons(self, addon, button_box):
        install_button = QPushButton(QIcon.fromTheme("list-add"), _("Install"))
        install_button.setFocusPolicy(Qt.NoFocus)
        install_button.clicked.connect(partial(self.__install, addon))
        button_box.addWidget(install_button)
        
        installed = QLabel("<i><small>{0}</small></i>".format(_("Addon is already installed")))
        button_box.addWidget(installed)
        
        self.__buttons[addon.identifier] = self.__OnlineAddonButtons(install_button, installed)
        
        if addon.local_addon is None:
            installed.setVisible(False)
        else:
            install_button.setVisible(False)
    
    @property
    def _addons(self):
        return Application().addons.online
    
    def __show_info(self, addon, checked=False):
        dialog = AddOnInfoDialog(self, addon)
        dialog.exec_()
    
    def __show_homepage(self, addon, checked=False):
        QDesktopServices.openUrl(QUrl(addon.homepage))
    
    def __install(self, addon, checked=False):
        dialog = InstallAddOnDialog(self, addon)
        if dialog.exec_() == InstallAddOnDialog.Accepted:
            self.__processes.run_process(addon.latest_version.install())
    
    def __addon_installed(self, event):
        if event.addon.identifier in self.__buttons:
            buttons = self.__buttons[event.addon.identifier]
            buttons.installed_info.setVisible(True)
            buttons.install.setVisible(False)
