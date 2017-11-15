from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTabWidget

from .onlineaddons import OnlineAddOnList
from .installedaddons import InstalledAddOnList
from .updateaddons import UpdateAddOnList
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
        
        tabs = QTabWidget()
        
        tabs.addTab(InstalledAddOnList(self.__processes), _("Installed Add-ons"))
        tabs.addTab(OnlineAddOnList(self.__processes), _("Online Add-ons"))
        tabs.addTab(UpdateAddOnList(), _("Updates"))
        
        layout.addWidget(tabs)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def sizeHint(self):
        return QSize(700, 450)
    
    def closeEvent(self, event):
        if self.isEnabled():
            super().closeEvent(event)
        else:
            event.ignore()
