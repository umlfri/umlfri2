from functools import partial

from PySide.QtCore import Qt, QMimeData
from PySide.QtGui import QTreeWidget, QTreeWidgetItem, QMenu
from umlfri2.application import Application
from umlfri2.application.commands.model import CreateElementCommand, CreateDiagramCommand
from umlfri2.application.events.application import LanguageChangedEvent
from umlfri2.application.events.model import ElementCreatedEvent, ObjectChangedEvent, DiagramCreatedEvent, \
    ProjectChangedEvent, ElementDeletedEvent, DiagramDeletedEvent
from umlfri2.application.events.solution import OpenProjectEvent, OpenSolutionEvent
from umlfri2.model import Diagram, ElementObject, Project
from umlfri2.qtgui.properties import PropertiesDialog, ProjectPropertiesDialog
from ..base import image_loader


class ProjectMimeData(QMimeData):
    def __init__(self, model_object):
        super().__init__()
        self.__model_object = model_object
    
    @property
    def model_object(self):
        return self.__model_object


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
        
        Application().event_dispatcher.subscribe(ElementCreatedEvent, self.__element_created)
        Application().event_dispatcher.subscribe(DiagramCreatedEvent, self.__diagram_created)
        Application().event_dispatcher.subscribe(ElementDeletedEvent, self.__element_deleted)
        Application().event_dispatcher.subscribe(DiagramDeletedEvent, self.__diagram_deleted)
        Application().event_dispatcher.subscribe(ObjectChangedEvent, self.__object_changed)
        Application().event_dispatcher.subscribe(ProjectChangedEvent, self.__project_changed)
        Application().event_dispatcher.subscribe(OpenProjectEvent, self.__project_open)
        Application().event_dispatcher.subscribe(OpenSolutionEvent, self.__solution_open)
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        
        self.__reload_texts()
    
    def reload(self):
        self.clear()
        
        if Application().solution is None:
            return
        
        for project in Application().solution.children:
            self.__reload_project(project)

    def __reload_project(self, project):
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
    
    def __element_deleted(self, event):
        item = self.__get_item(event.element)
        parent = item.parent()
        parent.removeChild(item)
    
    def __diagram_deleted(self, event):
        item = self.__get_item(event.diagram)
        parent = item.parent()
        parent.removeChild(item)
    
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
                    parent_item.insertChild(item_id, ProjectTreeItem(None, event.diagram))
                    break
        else:
            parent_item.addChild(ProjectTreeItem(parent_item, event.diagram))
        
        parent_item.setExpanded(True)
    
    def __object_changed(self, event):
        if isinstance(event.object, (ElementObject, Diagram)):
            item = self.__get_item(event.object)
            item.setText(0, event.object.get_display_name())
    
    def __project_changed(self, event):
        item = self.__get_item(event.project)
        item.setText(0, event.project.name)
    
    def __item_double_clicked(self, item, column):
        if isinstance(item, ProjectTreeItem):
            if isinstance(item.model_object, Diagram):
                Application().tabs.select_tab(item.model_object)
    
    def __show_tree_menu(self, position):
        item = self.itemAt(position)
        
        if item is not None:
            if isinstance(item, ProjectTreeItem):
                if isinstance(item.model_object, ElementObject):
                    menu = self.__create_element_menu(item.model_object)
                elif isinstance(item.model_object, Project):
                    menu = self.__create_project_menu(item.model_object)
                elif isinstance(item.model_object, Diagram):
                    menu = self.__create_diagram_menu(item.model_object)
                else:
                    menu = None
                
                if menu is not None:
                    menu.exec_(self.viewport().mapToGlobal(position))
    
    def __create_element_menu(self, element):
        metamodel = element.project.metamodel
        translation = metamodel.addon.get_translation(Application().language)
        
        menu = QMenu()
        
        sub_menu = menu.addMenu(_("Add diagram"))
        for diagram_type in metamodel.diagram_types:
            action = sub_menu.addAction(translation.translate(diagram_type))
            action.setIcon(image_loader.load_icon(diagram_type.icon))
            action.triggered.connect(partial(self.__create_diagram_action, diagram_type, element))
        
        sub_menu = menu.addMenu(_("Add element"))
        for element_type in metamodel.element_types:
            action = sub_menu.addAction(translation.translate(element_type))
            action.setIcon(image_loader.load_icon(element_type.icon))
            action.triggered.connect(partial(self.__create_element_action, element_type, element))
        
        menu.addSeparator()
        menu.addAction(_("Properties...")).triggered.connect(partial(self.__open_properties_action, element))
        
        return menu
    
    def __create_project_menu(self, project):
        metamodel = project.metamodel
        translation = metamodel.addon.get_translation(Application().language)
        
        menu = QMenu()
        
        sub_menu = menu.addMenu(_("Add element"))
        for element_type in metamodel.element_types:
            action = sub_menu.addAction(translation.translate(element_type))
            action.setIcon(image_loader.load_icon(element_type.icon))
            action.triggered.connect(partial(self.__create_element_action, element_type, project))
        
        menu.addSeparator()
        menu.addAction(_("Properties...")).triggered.connect(partial(self.__open_project_properties_action, project))
        
        return menu
    
    def __create_diagram_menu(self, diagram):
        menu = QMenu()
        
        show = menu.addAction(_("Show diagram in tab"))
        show.triggered.connect(partial(self.__show_diagram_action, diagram))
        menu.setDefaultAction(show)
        
        menu.addSeparator()
        menu.addAction(_("Properties...")).triggered.connect(partial(self.__open_properties_action, diagram))
        
        return menu
    
    def __show_diagram_action(self, diagram, checked=False):
        Application().tabs.select_tab(diagram)
    
    def __open_properties_action(self, object, checked=False):
        PropertiesDialog.open_for(self.__main_window, object)
    
    def __open_project_properties_action(self, project, checked=False):
        ProjectPropertiesDialog.open_for(self.__main_window, project)
    
    def __create_element_action(self, element_type, parent, checked=False):
        command = CreateElementCommand(parent, element_type)
        Application().commands.execute(command)
    
    def __create_diagram_action(self, element_type, parent, checked=False):
        command = CreateDiagramCommand(parent, element_type)
        Application().commands.execute(command)
        Application().tabs.select_tab(command.diagram)
    
    def __solution_open(self, event):
        self.reload()
    
    def __project_open(self, event):
        self.__reload_project(event.project)
    
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
    
    def mimeData(self, items):
        if items and isinstance(items[0], ProjectTreeItem):
            ret = super().mimeData([items[0]])
            formats = ret.formats()
            data = ret.data(formats[0])
            ret = ProjectMimeData(items[0].model_object)
            self.__mime_data_temp = ret # QT does not keep the reference!
            ret.setData(formats[0], data)
            return ret
        else:
            return None
    
    def __reload_texts(self):
        pass
