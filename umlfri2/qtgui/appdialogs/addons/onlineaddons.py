from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel

from umlfri2.application import Application
from .listwidget import AddOnListWidget


class OnlineAddOnList(AddOnListWidget):
    def _addon_button_factory(self):
        return self
    
    def _addon_content_menu(self, addon):
        return None
    
    def add_buttons(self, addon, button_box):
        if addon.local_addon is None:
            install_button = QPushButton(QIcon.fromTheme("list-add"), _("Install"))
            install_button.setFocusPolicy(Qt.NoFocus)
            button_box.addWidget(install_button)
        else:
            installed = QLabel("<i><small>{0}</small></i>".format(_("Addon is already installed")))
            button_box.addWidget(installed)
    
    @property
    def _addons(self):
        return Application().addons.online
    
    def _get_version(self, addon):
        return addon.latest_version.version
