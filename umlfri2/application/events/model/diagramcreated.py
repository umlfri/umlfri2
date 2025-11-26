from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Diagram


class DiagramCreatedEvent(Event):
    def __init__(self, diagram: Diagram, index: Optional[int] = None, indirect: bool = False) -> None:
        self.__diagram = diagram
        self.__index = index
        self.__indirect = indirect
    
    @property
    def diagram(self) -> Diagram:
        return self.__diagram
    
    @property
    def index(self) -> Optional[int]:
        return self.__index
    
    @property
    def indirect(self) -> bool:
        return self.__indirect
    
    def get_opposite(self) -> DiagramDeletedEvent:
        from .diagramdeleted import DiagramDeletedEvent
        
        return DiagramDeletedEvent(self.__diagram, self.__index, self.__indirect)
