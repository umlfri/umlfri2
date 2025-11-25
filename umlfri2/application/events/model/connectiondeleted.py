from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import ConnectionObject


class ConnectionDeletedEvent(Event):
    def __init__(self, connection: ConnectionObject, indirect: bool = False) -> None:
        self.__connection = connection
        self.__indirect = indirect
    
    @property
    def connection(self) -> ConnectionObject:
        return self.__connection
    
    @property
    def indirect(self) -> bool:
        return self.__indirect
    
    def get_opposite(self) -> ConnectionCreatedEvent:
        from .connectioncreated import ConnectionCreatedEvent
        
        return ConnectionCreatedEvent(self.__connection, self.__indirect)
