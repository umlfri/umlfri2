from .diagrammenu import ProjectTreeDiagramMenu as ProjectTreeDiagramMenu
from .elementmenu import ProjectTreeElementMenu as ProjectTreeElementMenu
from .mimedata import ProjectMimeData as ProjectMimeData
from .projectmenu import ProjectTreeProjectMenu as ProjectTreeProjectMenu
from .treeitem import ProjectTreeItem as ProjectTreeItem
from PyQt5.QtWidgets import QTreeWidget
from umlfri2.application import Application as Application
from umlfri2.application.commands.model.movenode import MoveNodeCommand as MoveNodeCommand
from umlfri2.application.events.application import ItemSelectedEvent as ItemSelectedEvent
from umlfri2.application.events.model import DiagramCreatedEvent as DiagramCreatedEvent, DiagramDeletedEvent as DiagramDeletedEvent, ElementCreatedEvent as ElementCreatedEvent, ElementDeletedEvent as ElementDeletedEvent, NodeMovedEvent as NodeMovedEvent, ObjectDataChangedEvent as ObjectDataChangedEvent, ProjectChangedEvent as ProjectChangedEvent
from umlfri2.application.events.solution import CloseSolutionEvent as CloseSolutionEvent, OpenProjectEvent as OpenProjectEvent, OpenSolutionEvent as OpenSolutionEvent, RemoveProjectEvent as RemoveProjectEvent
from umlfri2.application.events.tabs import OpenTabEvent as OpenTabEvent
from umlfri2.model import Diagram as Diagram, ElementObject as ElementObject, Project as Project

class ProjectTree(QTreeWidget):
    def __init__(self, main_window) -> None: ...
    def reload(self) -> None: ...
    def mimeData(self, items): ...
    def dropMimeData(self, parent, index, data, action): ...
