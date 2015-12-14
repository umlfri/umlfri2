from umlfri2.application.commands.diagram import MoveConnectionPointCommand
from umlfri2.types.geometry import PathBuilder
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveConnectionPointAction(Action):
    def __init__(self, connection, index):
        super().__init__()
        self.__connection = connection
        self.__index = index
        self.__path = None
    
    @property
    def path(self):
        return self.__path
    
    @property
    def cursor(self):
        return DrawingAreaCursor.move
    
    def mouse_down(self, point):
        self.__points = list(self.__connection.get_points(self.application.ruler, element_centers=True))
        self.__build_path()
        self.__old_point = point
    
    def mouse_move(self, point):
        vector = point - self.__old_point
        self.__points[self.__index] += vector
        self.__build_path()
        self.__old_point = point
    
    def mouse_up(self):
        old_points = list(self.__connection.get_points(self.application.ruler, element_centers=True))
        command = MoveConnectionPointCommand(
            self.__connection,
            self.__index,
            self.__points[self.__index] - old_points[self.__index]
        )
        self.application.commands.execute(command)
        self._finish()
    
    def __build_path(self):
        path = PathBuilder()
        
        for idx, point in enumerate(self.__points):
            if idx == 0:
                path.move_to(point)
            else:
                path.line_to(point)
        
        self.__path = path.build()
