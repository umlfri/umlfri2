from umlfri2.application.events.diagram import ConnectionMovedEvent
from ..base import Command


class AddConnectionPointCommand(Command):
    def __init__(self, connection, index, position):
        self.__diagram_name = connection.diagram.get_display_name()
        self.__connection = connection
        self.__index = index
        self.__point_position = position
    
    @property
    def description(self):
        return "Added point to connection in diagram {0}".format(self.__diagram_name)

    def _do(self, ruler):
        self._redo(ruler)

    def _redo(self, ruler):
        self.__connection.add_point(ruler, self.__index, self.__point_position)
    
    def _undo(self, ruler):
        self.__connection.remove_point(ruler, self.__index)
    
    def get_updates(self):
        yield ConnectionMovedEvent(self.__connection)
