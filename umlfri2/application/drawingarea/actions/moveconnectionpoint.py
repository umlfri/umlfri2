from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveConnectionPointAction(Action):
    def __init__(self, connection, index):
        self.__connection = connection
        self.__index = index
    
    @property
    def connection(self):
        return self.__connection
    
    @property
    def index(self):
        return self.__index
    
    def get_cursor(self):
        return DrawingAreaCursor.move
