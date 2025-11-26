from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from umlfri2.application.events.model import DiagramDeletedEvent
from ..base import Command

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.model import Diagram, ElementObject
    from umlfri2.ufl.components.visual.canvas import Ruler


class DeleteDiagramCommand(Command):
    def __init__(self, diagram: Diagram) -> None:
        self.__parent = diagram.parent
        self.__diagram = diagram
    
    @property
    def description(self) -> str:
        return "Diagram deleted from the project"
    
    def _do(self, ruler: Ruler) -> None:
        self._redo(ruler)
    
    def _redo(self, ruler: Ruler) -> None:
        self.__parent.remove_child(self.__diagram)
    
    def _undo(self, ruler: Ruler) -> None:
        self.__parent.add_child(self.__diagram)
    
    def get_updates(self) -> Iterator[Event]:
        yield DiagramDeletedEvent(self.__diagram)
