from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QCheckBox, QListWidget, QPushButton

from umlfri2.application import Application
from umlfri2.types.version import Version


class SettingsDialogUpdates(QWidget):
    def __init__(self, dialog):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        self.__auto_check_gb = QGroupBox()
        layout.addWidget(self.__auto_check_gb)
        
        self.__auto_check_cb = QCheckBox()
        self.__auto_check_cb.setChecked(Application().config.auto_check_updates)
        
        auto_check_layout = QVBoxLayout()
        auto_check_layout.addWidget(self.__auto_check_cb)
        self.__auto_check_gb.setLayout(auto_check_layout)
        
        self.__ignored_gb = QGroupBox()
        
        ignored_layout = QVBoxLayout()
        
        self.__ignored_lst = QListWidget()
        self.__ignored_lst.setSelectionMode(QListWidget.SingleSelection)
        
        for ver in sorted(Application().config.ignored_versions):
            self.__ignored_lst.addItem(str(ver))
        
        self.__ignored_lst.itemSelectionChanged.connect(self.__ignored_selection_changed)
        
        ignored_layout.addWidget(self.__ignored_lst)
        
        self.__to_unignore = set()
        
        self.__unignore = QPushButton()
        self.__unignore.setEnabled(False)
        self.__unignore.setIcon(QIcon.fromTheme("edit-delete"))
        self.__unignore.clicked.connect(self.__unignore_version)
        ignored_layout.addWidget(self.__unignore)
        
        self.__ignored_gb.setLayout(ignored_layout)
        
        layout.addWidget(self.__ignored_gb)
        
        self.setLayout(layout)
        
        self.reload_texts()
    
    def __ignored_selection_changed(self):
        self.__unignore.setEnabled(len(self.__ignored_lst.selectedItems()) == 1)
    
    def __unignore_version(self, checked=False):
        if len(self.__ignored_lst.selectedItems()) != 1:
            return
        
        item, = self.__ignored_lst.selectedItems()
        self.__to_unignore.add(Version(item.text()))
        self.__ignored_lst.takeItem(self.__ignored_lst.row(item))
    
    @staticmethod
    def get_name():
        return _("Updates")
    
    def apply_settings(self):
        Application().config.auto_check_updates = self.__auto_check_cb.isChecked()
        Application().config.unignore_versions(*self.__to_unignore)
    
    def reload_texts(self):
        self.__auto_check_gb.setTitle(_("Automatic Updates"))
        self.__auto_check_cb.setText(_("Check for UML .FRI updates at the application startup"))
        
        self.__ignored_gb.setTitle(_("Ignored Versions"))
        self.__unignore.setText(_("Remove version"))
