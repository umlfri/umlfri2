from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model.connection import ConnectionVisual


class ConnectionHiddenEvent(Event):
    def __init__(self, connection: ConnectionVisual) -> None:
        self.__connection = connection
    
    @property
    def connection(self) -> ConnectionVisual:
        return self.__connection
    
    def get_chained(self) -> Iterator[Event]:
        from .diagramchanged import DiagramChangedEvent
        
        yield DiagramChangedEvent(self.__connection.diagram)
    
    def get_opposite(self) -> ConnectionShownEvent:
        from .connectionshown import ConnectionShownEvent
        
        return ConnectionShownEvent(self.__connection)
