from PySide.QtCore import Qt
from PySide.QtGui import QTreeWidget
from umlfri2.application import Application
from umlfri2.application.commands.model.movenode import MoveNodeCommand
from umlfri2.application.events.application import ItemSelectedEvent
from umlfri2.application.events.model import ElementCreatedEvent, ObjectDataChangedEvent, DiagramCreatedEvent, \
    ProjectChangedEvent, ElementDeletedEvent, DiagramDeletedEvent, NodeMovedEvent
from umlfri2.application.events.solution import OpenProjectEvent, OpenSolutionEvent
from umlfri2.model import Diagram, ElementObject, Project
from .mimedata import ProjectMimeData
from .treeitem import ProjectTreeItem
from .diagrammenu import ProjectTreeDiagramMenu
from .projectmenu import ProjectTreeProjectMenu
from .elementmenu import ProjectTreeElementMenu


class ProjectTree(QTreeWidget):
    def __init__(self, main_window):
        super().__init__()
        self.__main_window = main_window
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__show_tree_menu)
        self.header().close()
        self.itemSelectionChanged.connect(self.__item_selected)
        self.itemActivated.connect(self.__item_activated)
        self.setDragDropMode(QTreeWidget.DragDrop)
        self.invisibleRootItem().setFlags(0)
        
        Application().event_dispatcher.subscribe(ElementCreatedEvent, self.__element_created)
        Application().event_dispatcher.subscribe(DiagramCreatedEvent, self.__diagram_created)
        Application().event_dispatcher.subscribe(ElementDeletedEvent, self.__element_deleted)
        Application().event_dispatcher.subscribe(DiagramDeletedEvent, self.__diagram_deleted)
        Application().event_dispatcher.subscribe(ObjectDataChangedEvent, self.__object_changed)
        Application().event_dispatcher.subscribe(ProjectChangedEvent, self.__project_changed)
        Application().event_dispatcher.subscribe(OpenProjectEvent, self.__project_open)
        Application().event_dispatcher.subscribe(OpenSolutionEvent, self.__solution_open)
        Application().event_dispatcher.subscribe(ItemSelectedEvent, self.__element_selected)
        Application().event_dispatcher.subscribe(NodeMovedEvent, self.__node_moved)
    
    def reload(self):
        self.clear()
        
        if Application().solution is None:
            return
        
        for project in Application().solution.children:
            self.__reload_project(project)

    def __reload_project(self, project):
        item = ProjectTreeItem(project)
        for element in project.children:
            self.__reload_element(item, element)
        self.addTopLevelItem(item)
        item.setExpanded(True)
        item.refresh()

    def __reload_element(self, parent, element, index=None):
        item = ProjectTreeItem(element)
        
        for child_diagram in element.diagrams:
            child_item = ProjectTreeItem(child_diagram)
            item.addChild(child_item)
            child_item.refresh()
        
        for child_element in element.children:
            self.__reload_element(item, child_element)
        
        if index is None:
            parent.addChild(item)
        else:
            if isinstance(element.parent, ElementObject):
                index += element.parent.diagram_count
            parent.insertChild(index, item)
        
        item.refresh()
    
    def __reload_diagram(self, parent, diagram, index=None):
        child_item = ProjectTreeItem(diagram)
        
        if index is not None:
            parent.insertChild(index, child_item)
        else:
            for item_id in range(parent.childCount()):
                item = parent.child(item_id)
                
                if isinstance(item, ProjectTreeItem):
                    if isinstance(item.model_object, ElementObject):
                        parent.insertChild(item_id, child_item)
                        break
            else:
                parent.addChild(child_item)
        
        child_item.refresh()
    
    def __element_deleted(self, event):
        if event.indirect:
            return
        
        item = self.__get_item(event.element)
        parent = item.parent()
        parent.removeChild(item)
    
    def __diagram_deleted(self, event):
        if event.indirect:
            return
        
        item = self.__get_item(event.diagram)
        parent = item.parent()
        parent.removeChild(item)
    
    def __element_created(self, event):
        if event.indirect:
            return
        
        parent_item = self.__get_item(event.element.parent)
        
        self.__reload_element(parent_item, event.element, event.index)
        
        parent_item.setExpanded(True)
    
    def __diagram_created(self, event):
        if event.indirect:
            return
        
        parent_item = self.__get_item(event.diagram.parent)
        
        self.__reload_diagram(parent_item, event.diagram, event.index)
        
        parent_item.setExpanded(True)
    
    def __object_changed(self, event):
        if isinstance(event.object, (ElementObject, Diagram)):
            item = self.__get_item(event.object)
            item.refresh()
    
    def __project_changed(self, event):
        item = self.__get_item(event.project)
        item.refresh()
    
    def __element_selected(self, event):
        if event.item is None:
            self.setCurrentItem(None)
        else:
            item = self.__get_item(event.item)
            
            if self.currentItem() is item:
                return
            
            parent = item.parent()
            while parent is not None:
                parent.setExpanded(True)
                parent = parent.parent()
            
            self.setCurrentItem(item)
    
    def __node_moved(self, event):
        old_parent_item = self.__get_item(event.old_parent)
        parent_item = self.__get_item(event.new_parent)
        
        for item_id in range(old_parent_item.childCount()):
            item = old_parent_item.child(item_id)
            if isinstance(item, ProjectTreeItem) and item.model_object is event.node:
                old_parent_item.removeChild(item)
                break
        else:
            raise Exception
        
        old_parent_item.removeChild(item)
        
        if isinstance(event.node, ElementObject):
            self.__reload_element(parent_item, event.node, event.new_index)
        else:
            self.__reload_diagram(parent_item, event.node, event.new_index)
    
    def __item_activated(self, item, column):
        if isinstance(item, ProjectTreeItem):
            if isinstance(item.model_object, Diagram):
                Application().tabs.select_tab(item.model_object)
    
    def __item_selected(self):
        item = self.currentItem()
        if isinstance(item, ProjectTreeItem):
            Application().select_item(item.model_object)
        else:
            Application().select_item(None)
    
    def __show_tree_menu(self, position):
        item = self.itemAt(position)
        
        if item is not None:
            if isinstance(item, ProjectTreeItem):
                if isinstance(item.model_object, ElementObject):
                    menu = ProjectTreeElementMenu(self.__main_window, item.model_object)
                elif isinstance(item.model_object, Project):
                    menu = ProjectTreeProjectMenu(self.__main_window, item.model_object)
                elif isinstance(item.model_object, Diagram):
                    menu = ProjectTreeDiagramMenu(self.__main_window, item.model_object)
                else:
                    menu = None
                
                if menu is not None:
                    menu.exec_(self.viewport().mapToGlobal(position))
    
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
            object = items[0].model_object
            
            ret = ProjectMimeData(object)
            self.__mime_data_temp = ret # QT does not keep the reference!
            ret.setData(formats[0], data)

            self.__enable_drop_for(
                self.invisibleRootItem(),
                self.__get_item(object.project),
                self.__get_item(object),
                False,
                isinstance(object, ElementObject)
            )
            
            return ret
        else:
            return None
    
    def __enable_drop_for(self, node, enabled_node, disabled_node, enabled, enable_for_project):
        if isinstance(node, ProjectTreeItem):
            if isinstance(node.model_object, Project) and enable_for_project:
                node.set_drop_enabled(enabled)
            elif isinstance(node.model_object, ElementObject):
                node.set_drop_enabled(enabled)
            else:
                node.set_drop_enabled(False)
        
        for item_id in range(node.childCount()):
            child = node.child(item_id)
            
            if child is enabled_node:
                self.__enable_drop_for(child, enabled_node, disabled_node, True, enable_for_project)
            elif child is disabled_node:
                self.__enable_drop_for(child, enabled_node, disabled_node, False, enable_for_project)
            else:
                self.__enable_drop_for(child, enabled_node, disabled_node, enabled, enable_for_project)
    
    def dropMimeData(self, parent, index, data, action):
        if not isinstance(parent, ProjectTreeItem):
            return False
        
        if not isinstance(data, ProjectMimeData):
            return False
        
        if isinstance(data.model_object, ElementObject) and isinstance(parent.model_object, ElementObject):
            index -= parent.model_object.diagram_count
        
        if data.model_object.parent is parent.model_object:
            if parent.model_object.get_child_index(data.model_object) < index:
                index -= 1
    
        if index < 0:
            index = 0
        
        if isinstance(data.model_object, ElementObject) and index >= parent.model_object.children_count:
            index = parent.model_object.children_count - 1
        elif isinstance(data.model_object, Diagram) and index >= parent.model_object.diagram_count:
            index = parent.model_object.diagram_count - 1
        
        command = MoveNodeCommand(data.model_object, parent.model_object, index)
        Application().commands.execute(command)
        
        return True
