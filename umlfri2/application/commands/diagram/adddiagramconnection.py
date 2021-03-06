from umlfri2.application.events.diagram import ConnectionShownEvent
from umlfri2.application.events.model import ConnectionCreatedEvent
from ..base import Command


class AddDiagramConnectionCommand(Command):
    def __init__(self, diagram, connection_type, source_element, destination_element, points):
        self.__diagram_name = diagram.get_display_name()
        self.__diagram = diagram
        self.__connection_type = connection_type
        self.__source_element = source_element.object
        self.__destination_element = destination_element.object
        self.__points = list(points)
        self.__connection_visual = None
        self.__connection_object = None
    
    @property
    def description(self):
        return "Adding connection '{0}' to diagram '{1}'".format(self.__connection_type.id, self.__diagram_name)
    
    def _do(self, ruler):
        self.__connection_object = self.__source_element.connect_with(self.__connection_type, self.__destination_element)
        self.__connection_visual = self.__diagram.show(self.__connection_object)
        for point in self.__points:
            self.__connection_visual.add_point(ruler, None, point)
    
    def _redo(self, ruler):
        self.__source_element.reconnect(self.__connection_object)
        self.__diagram.add(self.__connection_visual)
    
    def _undo(self, ruler):
        self.__source_element.disconnect(self.__connection_object)
        self.__diagram.remove(self.__connection_visual)
    
    @property
    def connection_visual(self):
        return self.__connection_visual
    
    @property
    def connection_object(self):
        return self.__connection_object
    
    def get_updates(self):
        yield ConnectionCreatedEvent(self.__connection_object)
        yield ConnectionShownEvent(self.__connection_visual)
