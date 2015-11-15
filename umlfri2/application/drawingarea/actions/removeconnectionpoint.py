from umlfri2.application.commands.diagram import RemoveConnectionPointCommand
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class RemoveConnectionPointAction(Action):
    def __init__(self, connection, index):
        super().__init__()
        self.__connection = connection
        self.__index = index
    
    @property
    def cursor(self):
        return DrawingAreaCursor.cross
    
    def mouse_down(self, drawing_area, application, point):
        command = RemoveConnectionPointCommand(
            self.__connection,
            self.__index
        )
        application.commands.execute(command)
        self._finish()
