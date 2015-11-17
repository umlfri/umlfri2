from PySide.QtGui import QTreeWidget, QTreeWidgetItem

from umlfri2.application import Application
from umlfri2.application.commands.model import ApplyPatchCommand
from umlfri2.application.events.project import ElementCreatedEvent
from umlfri2.model import Diagram, ElementObject
from umlfri2.qtgui.properties import PropertiesDialog
from umlfri2.ufl.dialog import UflDialog
from ..base import image_loader


class ProjectTreeItem(QTreeWidgetItem):
    def __init__(self, parent, values, model_object): 
        super().__init__(parent, values)
        self.__model_object = model_object
    
    @property
    def model_object(self):
        return self.__model_object


class ProjectTree(QTreeWidget):
    def __init__(self, main_window):
        super().__init__()
        self.__main_window = main_window
        self.header().close()
        self.itemDoubleClicked.connect(self.__item_double_clicked)
        self.setExpandsOnDoubleClick(False)
        
        Application().event_dispatcher.register(ElementCreatedEvent, self.__element_created)
    
    def reload(self):
        self.clear()
        for project in Application().solution.children:
            item = ProjectTreeItem(self, [project.name], project)
            item.setIcon(0, image_loader.load_icon(project.metamodel.addon.icon))
            
            for element in project.children:
                self.__reload_element(item, element)
            item.setExpanded(True)
            self.addTopLevelItem(item)
    
    def __reload_element(self, parent, element):
        item = ProjectTreeItem(parent, [element.get_display_name()], element)
        item.setIcon(0, image_loader.load_icon(element.type.icon))
        
        for child_diagram in element.diagrams:
            child = ProjectTreeItem(item, [child_diagram.get_display_name()], child_diagram)
            child.setIcon(0, image_loader.load_icon(child_diagram.type.icon))
            item.addChild(child)
        
        for child_element in element.children:
            self.__reload_element(item, child_element)
        parent.addChild(item)
    
    def __element_created(self, event):
        self.reload() # TODO: add only the element
    
    def __item_double_clicked(self, item, column):
        if isinstance(item, ProjectTreeItem):
            if isinstance(item.model_object, Diagram):
                Application().tabs.select_tab(item.model_object)
            elif isinstance(item.model_object, ElementObject):
                self.__edit(item.model_object)

    def __edit(self, model_object):
        dialog = UflDialog(model_object.data.type)
        dialog.associate(model_object.data)
        qt_dialog = PropertiesDialog(self.__main_window, dialog)
        qt_dialog.setModal(True)
        if qt_dialog.exec_() == PropertiesDialog.Accepted:
            dialog.finish()
            command = ApplyPatchCommand(model_object, dialog.make_patch())
            Application().commands.execute(command)
            self.update()
    
    def reload_texts(self):
        pass
