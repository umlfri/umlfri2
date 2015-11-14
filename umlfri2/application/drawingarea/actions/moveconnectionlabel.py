from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveConnectionLabelAction(Action):
    def __init__(self, connection, id):
        super().__init__()
        self.__connection = connection
        self.__id = id
    
    @property
    def cursor(self):
        return DrawingAreaCursor.move
