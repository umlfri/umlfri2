from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveConnectionPointAction(Action):
    def __init__(self, connection, index):
        super().__init__()
        self.__connection = connection
        self.__index = index
    
    @property
    def cursor(self):
        return DrawingAreaCursor.move
