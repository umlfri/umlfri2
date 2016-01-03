from PySide.QtCore import Qt
from PySide.QtGui import QTableWidgetItem

from umlfri2.application import Application
from umlfri2.application.commands.model import ChangeProjectNameCommand
from .tabletab import TableTab


class ProjectTab(TableTab):
    __project = None
    
    def __init__(self, project):
        super().__init__()
        
        self.setRowCount(1)
        self.itemChanged.connect(self.__item_changed)
        
        self.setItem(0, 1, QTableWidgetItem(_(project.name)))
        
        self.__project = project
    
    def __item_changed(self, item):
        if self.__project is None:
            return
        
        if item.column() != 1:
            return
        
        if item.row() == 0:
            command = ChangeProjectNameCommand(self.__project, item.text())
            Application().commands.execute(command)
    
    def reload_texts(self):
        super().reload_texts()
        
        name = QTableWidgetItem(_("Name"))
        name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.setItem(0, 0, name)
    
    @property
    def label(self):
        return _("General")
