from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from umlfri2.model import Project
from umlfri2.qtgui.base import image_loader


class ProjectTreeItem(QTreeWidgetItem):
    def __init__(self, model_object): 
        super().__init__(None)
        self.__model_object = model_object
        
        if isinstance(model_object, Project):
            self.setIcon(0, image_loader.load_icon(model_object.metamodel.addon.icon))
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        else:
            self.setIcon(0, image_loader.load_icon(model_object.type.icon))
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
    
    @property
    def model_object(self):
        return self.__model_object
    
    def refresh(self):
        if isinstance(self.__model_object, Project):
            name = self.__model_object.name
        else:
            name = self.__model_object.get_display_name()
        
        self.setText(0, name)
        self.setHidden(name is None)
    
    def set_drop_enabled(self, enabled):
        if enabled:
            self.setFlags(self.flags() | Qt.ItemIsDropEnabled)
        else:
            self.setFlags(self.flags() & ~Qt.ItemIsDropEnabled)
