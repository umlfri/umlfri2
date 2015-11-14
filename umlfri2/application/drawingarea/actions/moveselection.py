from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveSelectionAction(Action):
    def get_cursor(self):
        return DrawingAreaCursor.move
