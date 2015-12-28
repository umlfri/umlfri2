from PySide.QtCore import Qt
from PySide.QtGui import QTreeWidgetItem

from umlfri2.model import Project
from umlfri2.qtgui.base import image_loader


class ProjectTreeItem(QTreeWidgetItem):
    def __init__(self, parent, model_object): 
        super().__init__(parent)
        self.__model_object = model_object
        
        if isinstance(model_object, Project):
            self.setText(0, model_object.name)
            self.setIcon(0, image_loader.load_icon(model_object.metamodel.addon.icon))
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        else:
            self.setText(0, model_object.get_display_name())
            self.setIcon(0, image_loader.load_icon(model_object.type.icon))
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
    
    @property
    def model_object(self):
        return self.__model_object
