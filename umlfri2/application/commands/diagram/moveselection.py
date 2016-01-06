from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent
from ..base import Command, CommandNotDone


class MoveSelectionCommand(Command):
    def __init__(self, selection, delta):
        self.__diagram_name = selection.diagram.get_display_name()
        self.__elements = set(selection.selected_elements)
        self.__connections = set()
        for element in self.__elements:
            for connection in element.connections:
                if connection.source in self.__elements and connection.destination in self.__elements:
                    self.__connections.add(connection)
        self.__delta = delta
        self.__element_positions = []
        self.__connection_points = []
    
    @property
    def description(self):
        return "Selection in diagram '{0}' moved".format(self.__diagram_name)

    def _do(self, ruler):
        if not self.__delta:
            raise CommandNotDone
        
        self.__element_positions = []
        for element in self.__elements:
            self.__element_positions.append((element, element.get_position(ruler)))
        
        for connection in self.__connections:
            self.__connection_points.append((connection, list(connection.get_points(ruler, False))))
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        for element, position in self.__element_positions:
            element.move(ruler, position + self.__delta)
        
        for connection, points in self.__connection_points:
            for idx, point in enumerate(points):
                connection.move_point(ruler, idx + 1, point + self.__delta)
    
    def _undo(self, ruler):
        for element, position in self.__element_positions:
            element.move(ruler, position)
        
        for connection, points in self.__connection_points:
            for idx, point in enumerate(points):
                connection.move_point(ruler, idx + 1, point)
    
    def get_updates(self):
        for element in self.__elements:
            yield ElementResizedMovedEvent(element)
