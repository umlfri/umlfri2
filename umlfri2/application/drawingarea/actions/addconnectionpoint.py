from umlfri2.application.commands.diagram import AddConnectionPointCommand
from umlfri2.types.geometry import PathBuilder
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class AddConnectionPointAction(Action):
    def __init__(self, connection, index):
        super().__init__()
        self.__connection = connection
        self.__index = index
        self.__points = []
        self.__point = None
        self.__path = None
    
    @property
    def path(self):
        return self.__path
    
    @property
    def cursor(self):
        return DrawingAreaCursor.cross
    
    def mouse_down(self, drawing_area, application, point):
        self.__points = list(self.__connection.get_points(application.ruler, element_centers=True))
        self.__build_path()
    
    def mouse_move(self, drawing_area, application, point):
        self.__point = point
        self.__build_path()
    
    def mouse_up(self, drawing_area, application):
        command = AddConnectionPointCommand(
            self.__connection,
            self.__index,
            self.__point
        )
        application.commands.execute(command)
        self._finish()
    
    def __build_path(self):
        path = PathBuilder()
        
        for idx, point in enumerate(self.__points):
            if idx == 0:
                path.move_to(point)
            else:
                if idx == self.__index and self.__point is not None:
                    path.line_to(self.__point)
                path.line_to(point)
        
        self.__path = path.build()
