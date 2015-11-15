from umlfri2.application.commands.base import Command
from umlfri2.application.events.diagram import ConnectionMovedEvent


class MoveConnectionLabelCommand(Command):
    def __init__(self, connection_label, delta):
        self.__diagram_name = connection_label.connection.diagram.get_display_name()
        self.__connection_label = connection_label
        self.__delta = delta
        self.__label_position = None
    
    @property
    def description(self):
        return "Moved label on connection in diagram {0}".format(self.__diagram_name)
    
    def _do(self, ruler):
        self.__label_position = self.__connection_label.get_position(ruler)
        self._redo(ruler)
    
    def _redo(self, ruler):
        self.__connection_label.move(ruler, self.__label_position + self.__delta)
    
    def _undo(self, ruler):
        self.__connection_label.move(ruler, self.__label_position)
    
    def get_updates(self):
        yield ConnectionMovedEvent(self.__connection_label.connection)
