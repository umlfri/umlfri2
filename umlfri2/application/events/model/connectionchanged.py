from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import ConnectionObject


class ConnectionChangedEvent(Event):
    def __init__(self, connection: ConnectionObject) -> None:
        self.__connection = connection
    
    @property
    def connection(self) -> ConnectionObject:
        return self.__connection
    
    def get_opposite(self) -> ConnectionChangedEvent:
        return ConnectionChangedEvent(self.__connection)
