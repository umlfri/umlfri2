from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTabWidget

from umlfri2.application import Application
from umlfri2.application.events.addon import AddOnInstalledEvent, AddOnUninstalledEvent, AddOnUpdatedEvent
from .onlineaddons import OnlineAddOnList
from .installedaddons import InstalledAddOnList
from .updateaddons import UpdateAddOnTab
from .process import AddOnProcessManager


class AddOnsDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle(_("Add-ons"))
        
        self.__processes = AddOnProcessManager(self)
        
        self.__main_window = main_window
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.button(QDialogButtonBox.Close).setText(_("Close"))
        
        button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        
        self.__tabs = QTabWidget()

        self.__tabs.addTab(InstalledAddOnList(self.__processes), _("Installed Add-ons"))
        self.__tabs.addTab(OnlineAddOnList(self.__processes), _("Online Add-ons"))
        
        self.__has_update_tab = False
        self.__refresh_update_tab()
        
        layout.addWidget(self.__tabs)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        Application().event_dispatcher.subscribe(AddOnInstalledEvent, self.__addon_list_changed)
        Application().event_dispatcher.subscribe(AddOnUninstalledEvent, self.__addon_list_changed)
        Application().event_dispatcher.subscribe(AddOnUpdatedEvent, self.__addon_list_changed)
    
    def sizeHint(self):
        return QSize(700, 450)
    
    def closeEvent(self, event):
        if self.isEnabled():
            super().closeEvent(event)
        else:
            event.ignore()
    
    def __addon_list_changed(self, event):
        self.__refresh_update_tab()
    
    def __refresh_update_tab(self):
        if any(Application().addons.online.updated_addons):
            if not self.__has_update_tab:
                self.__tabs.addTab(UpdateAddOnTab(self.__processes), _("Updates"))
            
            self.__has_update_tab = True
        else:
            if self.__has_update_tab:
                self.__tabs.removeTab(2)
            
            self.__has_update_tab = False
