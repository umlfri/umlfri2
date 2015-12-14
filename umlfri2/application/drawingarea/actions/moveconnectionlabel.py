from umlfri2.application.commands.diagram import MoveConnectionLabelCommand
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveConnectionLabelAction(Action):
    __box = None
    
    def __init__(self, connection, id):
        super().__init__()
        self.__connection = connection
        self.__id = id
    
    @property
    def cursor(self):
        return DrawingAreaCursor.move
    
    @property
    def box(self):
        return self.__box
    
    def mouse_down(self, point):
        self.__box = self.__connection.get_label(self.__id).get_bounds(self.application.ruler)
        self.__old_point = point
    
    def mouse_move(self, point):
        vector = point - self.__old_point
        self.__box += vector
        self.__old_point = point
    
    def mouse_up(self):
        old_bounds = self.__connection.get_label(self.__id).get_bounds(self.application.ruler)
        command = MoveConnectionLabelCommand(
            self.__connection.get_label(self.__id),
            self.__box.top_left - old_bounds.top_left
        )
        self.application.commands.execute(command)
        self._finish()
