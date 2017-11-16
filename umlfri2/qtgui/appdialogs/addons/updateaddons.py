from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from umlfri2.application import Application
from umlfri2.application.events.addon import AddOnInstalledEvent, AddOnUninstalledEvent
from .listwidget import AddOnListWidget


class UpdateAddOnList(AddOnListWidget):
    def __init__(self):
        super().__init__(check_boxes=True, show_prev_version=True)

        Application().event_dispatcher.subscribe(AddOnInstalledEvent, self.__addon_list_changed)
        Application().event_dispatcher.subscribe(AddOnUninstalledEvent, self.__addon_list_changed)
        
    @property
    def _addons(self):
        yield from Application().addons.online.updated_addons
    
    def _addon_button_factory(self):
        pass
    
    def _addon_content_menu(self, addon):
        pass

    def __addon_list_changed(self, event):
        self.refresh()


class UpdateAddOnTab(QWidget):
    def __init__(self):
        super().__init__()
        
        self.__addon_list = UpdateAddOnList()
        self.__addon_list.check_changed.connect(self.__addon_check_changed)
        
        self.__update_button = QPushButton(_("Update"))
        
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
