from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox

from .infowidget import AddOnInfoWidget


class AddOnInfoDialog(QDialog):
    def __init__(self, addon_window, addon):
        super().__init__(addon_window)
        self.__addon = addon
        
        layout = QVBoxLayout()
        
        layout.addWidget(AddOnInfoWidget(addon))
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.button(QDialogButtonBox.Close).setText(_("Close"))
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)
