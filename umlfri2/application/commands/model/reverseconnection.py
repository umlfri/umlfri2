from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from umlfri2.application.events.model import ConnectionChangedEvent
from ..base import Command

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.model import ConnectionObject


class ReverseConnectionCommand(Command):
    def __init__(self, connection: ConnectionObject) -> None:
        self.__connection = connection

    @property
    def description(self) -> str:
        return "Connection reversed"

    def _do(self, ruler: object) -> None:
        self.__connection.reverse()

    def _redo(self, ruler: object) -> None:
        self.__connection.reverse()

    def _undo(self, ruler: object) -> None:
        self.__connection.reverse()

    def get_updates(self) -> Iterator[Event]:
        yield ConnectionChangedEvent(self.__connection)
