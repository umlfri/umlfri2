from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel

from umlfri2.qtgui.base.hlinewidget import HLineWidget
from .infowidget import AddOnInfoWidget


class InstallAddOnDialog(QDialog):
    TIMEOUT = 3
    
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
        
        self.__button_yes = button_box.button(QDialogButtonBox.Yes)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        self.__timeout = self.TIMEOUT
        self.__timeout_timer = QTimer(self)
        self.__timeout_timer.timeout.connect(self.__timeout_timer_tick)
        self.__timeout_timer.start(1000)
        self.__timeout_timer_tick()
    
    def __timeout_timer_tick(self):
        if self.__timeout == 0:
            self.__timeout_timer.stop()
            self.__button_yes.setEnabled(True)
            self.__button_yes.setText(_("Yes"))
        else:
            self.__button_yes.setEnabled(False)
            self.__button_yes.setText(_("Yes ({0})".format(self.__timeout)))
            self.__timeout -= 1
p