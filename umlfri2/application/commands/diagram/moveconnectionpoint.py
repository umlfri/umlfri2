from umlfri2.application.events.diagram import ConnectionMovedEvent
from ..base import Command


class MoveConnectionPointCommand(Command):
    def __init__(self, connection, index, delta):
        self.__diagram_name = connection.diagram.get_display_name()
        self.__connection = connection
        self.__index = index
        self.__delta = delta
        self.__point_position = None
    
    @property
    def description(self):
        return "Moved point on connection in diagram {0}".format(self.__diagram_name)
    
    def _do(self, ruler):
        self.__point_position = self.__connection.get_point(ruler, self.__index)
        self._redo(ruler)
    
    def _redo(self, ruler):
        self.__connection.move_point(ruler, self.__index, self.__point_position + self.__delta)
    
    def _undo(self, ruler):
        self.__connection.move_point(ruler, self.__index, self.__point_position)
    
    def get_updates(self):
        yield ConnectionMovedEvent(self.__connection)
