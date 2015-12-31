from umlfri2.application.events.model import ConnectionChangedEvent
from ..base import Command


class ReverseConnectionCommand(Command):
    def __init__(self, connection):
        self.__connection = connection

    @property
    def description(self):
        return "Connection reversed"

    def _do(self, ruler):
        self.__connection.reverse()

    def _redo(self, ruler):
        self.__connection.reverse()

    def _undo(self, ruler):
        self.__connection.reverse()

    def get_updates(self):
        yield ConnectionChangedEvent(self.__connection)
