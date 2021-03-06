from umlfri2.application.events.model import ConnectionDeletedEvent
from ..diagram import HideConnectionCommand
from ..base import Command


class DeleteConnectionCommand(Command):
    def __init__(self, connection):
        self.__connection = connection
        self.__hide_commands = []
    
    @property
    def description(self):
        return "Connection deleted from the project"
    
    def _do(self, ruler):
        for visual in self.__connection.visuals:
            self.__hide_commands.append(HideConnectionCommand(visual.diagram, visual))
        
        self.__connection.source.remove_connection(self.__connection)
        if self.__connection.source is not self.__connection.destination:
            self.__connection.destination.remove_connection(self.__connection)
        
        for hide_command in self.__hide_commands:
            hide_command.do(ruler)
    
    def _redo(self, ruler):
        self.__connection.source.remove_connection(self.__connection)
        if self.__connection.source is not self.__connection.destination:
            self.__connection.destination.remove_connection(self.__connection)
        
        for hide_command in self.__hide_commands:
            hide_command.redo(ruler)
    
    def _undo(self, ruler):
        self.__connection.source.add_connection(self.__connection)
        if self.__connection.source is not self.__connection.destination:
            self.__connection.destination.add_connection(self.__connection)
        
        for hide_command in self.__hide_commands:
            hide_command.undo(ruler)
    
    def get_updates(self):
        yield ConnectionDeletedEvent(self.__connection)
        
        for hide_command in self.__hide_commands:
            yield from hide_command.get_updates()
