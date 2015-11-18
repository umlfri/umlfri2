from functools import partial

from PySide.QtCore import Qt
from PySide.QtGui import QTreeWidget, QTreeWidgetItem, QMenu
from umlfri2.application import Application
from umlfri2.application.commands.model import ApplyPatchCommand, CreateElementCommand, CreateDiagramCommand
from umlfri2.application.events.model import ElementCreatedEvent, ObjectChangedEvent, DiagramCreatedEvent
from umlfri2.model import Diagram, ElementObject, Project
from umlfri2.qtgui.properties import PropertiesDialog
from umlfri2.ufl.dialog import UflDialog
from ..base import image_loader


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


class ProjectTree(QTreeWidget):
    def __init__(self, main_window):
        super().__init__()
        self.__main_window = main_window
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__show_tree_menu)
        self.header().close()
        self.itemDoubleClicked.connect(self.__item_double_clicked)
        self.setExpandsOnDoubleClick(False)
        
        Application().event_dispatcher.register(ElementCreatedEvent, self.__element_created)
        Application().event_dispatcher.register(DiagramCreatedEvent, self.__diagram_created)
        Application().event_dispatcher.register(ObjectChangedEvent, self.__object_changed)
    
    def reload(self):
        self.clear()
        for project in Application().solution.children:
            item = ProjectTreeItem(self, project)
            
            for element in project.children:
                self.__reload_element(item, element)
            item.setExpanded(True)
            self.addTopLevelItem(item)
    
    def __reload_element(self, parent, element):
        item = ProjectTreeItem(parent, element)
        
        for child_diagram in element.diagrams:
            item.addChild(ProjectTreeItem(item, child_diagram))
        
        for child_element in element.children:
            self.__reload_element(item, child_element)
        
        parent.addChild(item)
    
    def __element_created(self, event):
        parent_item = self.__get_item(event.element.parent)
        
        self.__reload_element(parent_item, event.element)
        
        parent_item.setExpanded(True)
    
    def __diagram_created(self, event):
        parent_item = self.__get_item(event.diagram.parent)
        
        for item_id in range(parent_item.childCount()):
            item = parent_item.child(item_id)
            
            if isinstance(item, ProjectTreeItem):
                if isinstance(item.model_object, ElementObject):
                    parent_item.insertChild(item_id, ProjectTreeItem(parent_item, event.diagram))
                    break
        else:
            parent_item.addChild(ProjectTreeItem(parent_item, event.diagram))
        
        parent_item.setExpanded(True)
    
    def __object_changed(self, event):
        if isinstance(event.object, (ElementObject, Diagram)):
            item = self.__get_item(event.object)
            item.setText(0, event.object.get_display_name())
    
    def __item_double_clicked(self, item, column):
        if isinstance(item, ProjectTreeItem):
            if isinstance(item.model_object, Diagram):
                Application().tabs.select_tab(item.model_object)
            elif isinstance(item.model_object, ElementObject):
                self.__edit(item.model_object)
    
    def __show_tree_menu(self, position):
        item = self.itemAt(position)
        
        if item is not None:
            if isinstance(item, ProjectTreeItem):
                if isinstance(item.model_object, ElementObject):
                    menu = self.__create_element_menu(item.model_object)
                elif isinstance(item.model_object, Project):
                    menu = self.__create_project_menu(item.model_object)
                else:
                    menu = None
                
                if menu is not None:
                    menu.exec_(self.viewport().mapToGlobal(position))
    
    def __create_element_menu(self, element):
        metamodel = element.project.metamodel
        
        menu = QMenu()
        
        sub_menu = menu.addMenu(_("Add diagram"))
        for diagram_type in metamodel.diagram_types:
            # TODO: translation
            action = sub_menu.addAction(diagram_type.id)
            action.setIcon(image_loader.load_icon(diagram_type.icon))
            action.triggered.connect(partial(self.__create_diagram_action, diagram_type, element))
        
        sub_menu = menu.addMenu(_("Add element"))
        for element_type in metamodel.element_types:
            # TODO: translation
            action = sub_menu.addAction(element_type.id)
            action.setIcon(image_loader.load_icon(element_type.icon))
            action.triggered.connect(partial(self.__create_element_action, element_type, element))
        
        return menu
    
    def __create_project_menu(self, project):
        metamodel = project.metamodel
        
        menu = QMenu()
        
        sub_menu = menu.addMenu(_("Add element"))
        for element_type in metamodel.element_types:
            # TODO: translation
            action = sub_menu.addAction(element_type.id)
            action.setIcon(image_loader.load_icon(element_type.icon))
            action.triggered.connect(partial(self.__create_element_action, element_type, project))
        
        return menu
    
    def __create_element_action(self, element_type, parent, checked=False):
        command = CreateElementCommand(parent, element_type)
        Application().commands.execute(command)
    
    def __create_diagram_action(self, element_type, parent, checked=False):
        command = CreateDiagramCommand(parent, element_type)
        Application().commands.execute(command)
        Application().tabs.select_tab(command.diagram)
    
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
    
    def __get_item(self, element):
        if element.parent is None:
            for item_id in range(self.topLevelItemCount()):
                item = self.topLevelItem(item_id)
                
                if isinstance(item, ProjectTreeItem) and item.model_object is element:
                    return item
        else:
            parent_item = self.__get_item(element.parent)
            
            for item_id in range(parent_item.childCount()):
                item = parent_item.child(item_id)
                
                if isinstance(item, ProjectTreeItem) and item.model_object is element:
                    return item
        
        return None
    
    def reload_texts(self):
        pass
