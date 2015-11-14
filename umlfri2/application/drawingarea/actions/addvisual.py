from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class AddVisualAction(Action):
    def __init__(self, category, type):
        self.__category = category
        self.__type = type
    
    @property
    def category(self):
        return self.__category
    
    @property
    def type(self):
        return self.__type
    
    def get_cursor(self):
        return DrawingAreaCursor.arrow
