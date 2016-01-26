from umlfri2.application.commands.diagram import MoveConnectionPointCommand
from umlfri2.types.geometry import PathBuilder, Point
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveConnectionPointAction(Action):
    def __init__(self, connection, index):
        super().__init__()
        self.__connection = connection
        self.__index = index
        self.__path = None
        self.__alignment = None
        self.__aligned = None
    
    @property
    def path(self):
        return self.__path
    
    @property
    def cursor(self):
        return DrawingAreaCursor.move
    
    @property
    def horizontal_alignment_indicators(self):
        if self.__aligned is not None:
            yield from self.__aligned.horizontal_indicators
    
    @property
    def vertical_alignment_indicators(self):
        if self.__aligned is not None:
            yield from self.__aligned.vertical_indicators
    
    def align_to(self, alignment):
        self.__alignment = alignment
    
    def mouse_down(self, point):
        self.__points = list(self.__connection.get_points(self.application.ruler, element_centers=True))
        self.__alignment.ignore_point(self.__points[self.__index])
        self.__build_path()
    
    def mouse_move(self, point):
        x, y = point.x, point.y
        
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        point = Point(x, y)
        
        if self.__alignment is not None:
            self.__aligned = self.__alignment.align_point(point)
            point = self.__aligned.result
        else:
            self.__aligned = None
        
        self.__points[self.__index] = point
        self.__build_path()
    
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
