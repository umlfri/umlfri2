from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel

from umlfri2.qtgui.base.hlinewidget import HLineWidget
from .infowidget import AddOnInfoWidget


class InstallAddOnDialog(QDialog):
    def __init__(self, addon_window, online_addon):
        super().__init__(addon_window)
        self.__online_addon = online_addon
        
        layout = QVBoxLayout()
        
        layout.addWidget(AddOnInfoWidget(online_addon))
        
        layout.addWidget(HLineWidget())
        
        layout.addWidget(QLabel(_("Do you really want to install this addon?")))
        
        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_box.button(QDialogButtonBox.Yes).setText(_("Yes"))
        button_box.button(QDialogButtonBox.No).setText(_("No"))
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.accept)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)
