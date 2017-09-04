from umlfri2.application.events.diagram import ConnectionMovedEvent
from ..base import Command, CommandNotDone


class RemoveConnectionPointCommand(Command):
    def __init__(self, connection, index):
        self.__diagram_name = connection.diagram.get_display_name()
        self.__connection = connection
        self.__index = index
        self.__point_position = None
    
    @property
    def description(self):
        return "Removed point from connection in diagram {0}".format(self.__diagram_name)

    def _do(self, ruler):
        if self.__connection.is_identity and self.__connection.number_of_points_on_line < 2:
            raise CommandNotDone
        self.__point_position = self.__connection.get_point(ruler, self.__index)
        self._redo(ruler)

    def _redo(self, ruler):
        self.__connection.remove_point(ruler, self.__index)
    
    def _undo(self, ruler):
        self.__connection.add_point(ruler, self.__index, self.__point_position)
    
    def get_updates(self):
        yield ConnectionMovedEvent(self.__connection)
