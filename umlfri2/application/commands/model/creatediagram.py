from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING

from umlfri2.application.events.model import DiagramCreatedEvent
from ..base import Command

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.metamodel.diagramtype import DiagramType
    from umlfri2.model import ElementObject, Diagram
    from umlfri2.ufl.components.visual.canvas import Ruler


class CreateDiagramCommand(Command):
    def __init__(self, parent: ElementObject, diagram_type: DiagramType) -> None:
        self.__parent = parent
        self.__diagram_type = diagram_type
        self.__diagram = None
    
    @property
    def description(self) -> str:
        return "Creating diagram '{0}'".format(self.__diagram_type.id)
    
    def _do(self, ruler: Ruler) -> None:
        self.__diagram = self.__parent.create_child_diagram(self.__diagram_type)
    
    def _redo(self, ruler: Ruler) -> None:
        self.__parent.add_child(self.__diagram)
    
    def _undo(self, ruler: Ruler) -> None:
        self.__parent.remove_child(self.__diagram)
    
    @property
    def diagram(self) -> Optional[Diagram]:
        return self.__diagram
    
    def get_updates(self) -> Iterator[Event]:
        yield DiagramCreatedEvent(self.__diagram)
