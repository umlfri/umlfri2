from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QFileDialog, QTabWidget, QWidget

from umlfri2.application import Application
from umlfri2.datalayer import Storage

from .installedaddons import InstalledAddOnList


class AddOnsDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle(_("Add-ons"))
        
        self.__main_window = main_window
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.button(QDialogButtonBox.Close).setText(_("Close"))
        
        install_button = button_box.addButton(_("Install new..."), QDialogButtonBox.ActionRole)
        install_button.setDefault(False)
        install_button.setAutoDefault(False)
        install_button.clicked.connect(self.__install_addon)
        
        button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        
        tabs.addTab(InstalledAddOnList(), _("Installed Add-ons"))
        tabs.addTab(QWidget(), _("Online Add-ons"))
        tabs.addTab(QWidget(), _("Updates"))
        
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
    
    def __install_addon(self):
        file_name, filter = QFileDialog.getOpenFileName(
                self,
                caption=_("Install AddOn From File"),
                filter=_("UML .FRI 2 addons") + "(*.fria2)"
        )
        if file_name:
            Application().addons.local.install_addon(Storage.read_storage(file_name))
