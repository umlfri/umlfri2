import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QDialogButtonBox

from umlfri2.application import Application
from umlfri2.application.events.application import LanguageChangedEvent
from .general import SettingsDialogGeneral
from .updates import SettingsDialogUpdates


class SettingsDialog(QDialog):
    __tab_classes = [SettingsDialogGeneral, SettingsDialogUpdates]
    
    def __init__(self, main_window):
        super().__init__(main_window)
        if os.name == 'nt':
            self.setWindowTitle(_("Options"))
        else:
            self.setWindowTitle(_("Preferences"))

        layout = QVBoxLayout()
        
        self.__tabs = QTabWidget()
        layout.addWidget(self.__tabs)
        
        for tab_class in self.__tab_classes:
            self.__tabs.addTab(tab_class(self), "")
        
        self.__button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        
        self.__button_box.button(QDialogButtonBox.Apply).clicked.connect(self.__apply_clicked)

        self.__button_box.accepted.connect(self.__accept_clicked)
        self.__button_box.rejected.connect(self.reject)
        
        layout.addWidget(self.__button_box)
        
        self.setLayout(layout)

        Application().event_dispatcher.subscribe(LanguageChangedEvent, self.__language_changed)
        
        self.__reload_texts()
    
    def __apply_clicked(self, checked=False):
        self.__apply_settings()
    
    def __accept_clicked(self):
        self.__apply_settings()
        self.accept()
    
    def __apply_settings(self):
        for no in range(self.__tabs.count()):
            self.__tabs.widget(no).apply_settings()
    
    def __language_changed(self, event):
        self.__reload_texts()
    
    def __reload_texts(self):
        self.__button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        self.__button_box.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
        self.__button_box.button(QDialogButtonBox.Apply).setText(_("Apply"))

        for no in range(self.__tabs.count()):
            widget = self.__tabs.widget(no)
            widget.reload_texts()
            self.__tabs.setTabText(no, widget.get_name())
        
