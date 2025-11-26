from __future__ import annotations

from typing import Iterator, List, TYPE_CHECKING

from umlfri2.application.events.model import ConnectionDeletedEvent
from ..diagram import HideConnectionCommand
from ..base import Command

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.model import ConnectionObject
    from umlfri2.ufl.components.visual.canvas import Ruler


class DeleteConnectionCommand(Command):
    def __init__(self, connection: ConnectionObject) -> None:
        self.__connection = connection
        self.__hide_commands = []
    
    @property
    def description(self) -> str:
        return "Connection deleted from the project"
    
    def _do(self, ruler: Ruler) -> None:
        for visual in self.__connection.visuals:
            self.__hide_commands.append(HideConnectionCommand(visual.diagram, visual))
        
        self.__connection.source.remove_connection(self.__connection)
        if self.__connection.source is not self.__connection.destination:
            self.__connection.destination.remove_connection(self.__connection)
        
        for hide_command in self.__hide_commands:
            hide_command.do(ruler)
    
    def _redo(self, ruler: Ruler) -> None:
        self.__connection.source.remove_connection(self.__connection)
        if self.__connection.source is not self.__connection.destination:
            self.__connection.destination.remove_connection(self.__connection)
        
        for hide_command in self.__hide_commands:
            hide_command.redo(ruler)
    
    def _undo(self, ruler: Ruler) -> None:
        self.__connection.source.add_connection(self.__connection)
        if self.__connection.source is not self.__connection.destination:
            self.__connection.destination.add_connection(self.__connection)
        
        for hide_command in self.__hide_commands:
            hide_command.undo(ruler)
    
    def get_updates(self) -> Iterator[Event]:
        yield ConnectionDeletedEvent(self.__connection)
        
        for hide_command in self.__hide_commands:
            yield from hide_command.get_updates()
