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
        self.__snapping = None
        self.__snapped = None
    
    @property
    def path(self):
        return self.__path
    
    @property
    def cursor(self):
        return DrawingAreaCursor.move
    
    @property
    def horizontal_snapping_indicators(self):
        if self.__snapped is not None:
            yield from self.__snapped.horizontal_indicators
    
    @property
    def vertical_snapping_indicators(self):
        if self.__snapped is not None:
            yield from self.__snapped.vertical_indicators
    
    def snap_to(self, snapping):
        self.__snapping = snapping.ignore_point(self.__connection, self.__index).build()
    
    def mouse_down(self, point):
        self.__points = list(self.__connection.get_points(self.application.ruler, element_centers=True))
        self.__build_path()
    
    def mouse_move(self, point):
        x, y = point.x, point.y
        
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        point = Point(x, y)
        
        if self.__snapping is not None:
            self.__snapped = self.__snapping.snap_point(point)
            point = self.__snapped.point
        else:
            self.__snapped = None
        
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
