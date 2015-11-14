from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class SelectManyAction(Action):
    def get_cursor(self):
        return DrawingAreaCursor.arrow
