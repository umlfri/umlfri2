from functools import partial

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QPushButton, QLabel, QMenu

from umlfri2.application import Application
from .installdialog import InstallAddOnDialog
from .info import AddOnInfoDialog
from .listwidget import AddOnListWidget


class OnlineAddOnList(AddOnListWidget):
    def _addon_button_factory(self):
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
        if addon.local_addon is None:
            install_button = QPushButton(QIcon.fromTheme("list-add"), _("Install"))
            install_button.setFocusPolicy(Qt.NoFocus)
            install_button.clicked.connect(partial(self.__install, addon))
            button_box.addWidget(install_button)
        else:
            installed = QLabel("<i><small>{0}</small></i>".format(_("Addon is already installed")))
            button_box.addWidget(installed)
    
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
        dialog.exec_()
