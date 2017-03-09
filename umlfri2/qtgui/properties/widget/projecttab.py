from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

from umlfri2.application import Application
from umlfri2.application.commands.model import ChangeProjectNameCommand
from umlfri2.qtgui.properties.widget.selectionchangingwidgets import QSelectionChangingLineEdit
from .tabletab import TableTab


class ProjectTab(TableTab):
    __project = None
    
    def __init__(self, project):
        super().__init__()
        
        self.setRowCount(1)
        
        self.__name_widget = QSelectionChangingLineEdit(self, 0)
        self.__name_widget.lostFocus.connect(self.__name_changed)
        self.__name_widget.returnPressed.connect(self.__name_changed)
        
        self.setCellWidget(0, 1, self.__name_widget)
        
        self.__project = project
        
        self.content_updated()
    
    def __name_changed(self, value=None):
        command = ChangeProjectNameCommand(self.__project, self.__name_widget.text())
        Application().commands.execute(command)
    
    def reload_texts(self):
        super().reload_texts()
        
        name = QTableWidgetItem(_("Name"))
        name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.setItem(0, 0, name)
        
        self.content_updated()
    
    def reload_data(self):
        self.__name_widget.setText(self.__project.name)
        
        self.content_updated()
    
    @property
    def label(self):
        return _("General")
