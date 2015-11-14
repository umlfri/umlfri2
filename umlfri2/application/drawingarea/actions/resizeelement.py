from ..selectionpointposition import SelectionPointPosition
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class ResizeElementAction(Action):
    def __init__(self, element, horizontal, vertical):
        self.__element = element
        self.__horizontal = horizontal
        self.__vertical = vertical
    
    @property
    def element(self):
        return self.__element
    
    @property
    def horizontal(self):
        return self.__horizontal
    
    @property
    def vertical(self):
        return self.__vertical
    
    def get_cursor(self):
        if self.__horizontal == self.__vertical:
            return DrawingAreaCursor.mainDiagonalResize
        elif self.__horizontal == SelectionPointPosition.center:
            return DrawingAreaCursor.verticalResize
        elif self.__vertical == SelectionPointPosition.center:
            return DrawingAreaCursor.horizontalResize
        else:
            return DrawingAreaCursor.antiDiagonalResize
