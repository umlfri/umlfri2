from umlfri2.application.events.diagram import ConnectionHiddenEvent
from ..base import Command


class HideConnectionCommand(Command):
    def __init__(self, diagram, connection):
        self.__diagram_name = diagram.get_display_name()
        self.__diagram = diagram
        self.__connection = connection
        self.__z_order = None
    
    @property
    def description(self):
        return "Hiding selected connection from diagram {0}".format(self.__diagram_name)
    
    def _do(self, ruler):
        self.__z_order = self.__diagram.get_z_order(self.__connection)
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        self.__diagram.remove(self.__connection)
    
    def _undo(self, ruler):
        self.__diagram.add(self.__connection, z_order=self.__z_order)
    
    def get_updates(self):
        yield ConnectionHiddenEvent(self.__connection)
