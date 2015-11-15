from umlfri2.application.commands.diagram import ResizeMoveElementCommand
from umlfri2.types.geometry import Rectangle
from ..selectionpointposition import SelectionPointPosition
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class ResizeElementAction(Action):
    __box = None
    
    def __init__(self, element, horizontal, vertical):
        super().__init__()
        self.__element = element
        self.__horizontal = horizontal
        self.__vertical = vertical
    
    @property
    def box(self):
        return self.__box
    
    @property
    def cursor(self):
        if self.__horizontal == self.__vertical:
            return DrawingAreaCursor.mainDiagonalResize
        elif self.__horizontal == SelectionPointPosition.center:
            return DrawingAreaCursor.verticalResize
        elif self.__vertical == SelectionPointPosition.center:
            return DrawingAreaCursor.horizontalResize
        else:
            return DrawingAreaCursor.antiDiagonalResize
    
    def mouse_down(self, drawing_area, application, point):
        self.__box = drawing_area.selection.get_bounds(application.ruler)
        self.__old_point = point
    
    def mouse_move(self, drawing_area, application, point):
        x1 = self.__box.x1
        y1 = self.__box.y1
        x2 = self.__box.x2
        y2 = self.__box.y2
        
        vector = point - self.__old_point
        
        min_size = self.__element.get_minimal_size(application.ruler)
        
        if self.__horizontal == SelectionPointPosition.first:
            x1 += vector.x
            if x2 - x1 < min_size.width:
                x1 = x2 - min_size.width
        elif self.__horizontal == SelectionPointPosition.last:
            x2 += vector.x
            if x2 - x1 < min_size.width:
                x2 = x1 + min_size.width
        
        if self.__vertical == SelectionPointPosition.first:
            y1 += vector.y
            if y2 - y1 < min_size.height:
                y1 = y2 - min_size.height
        elif self.__vertical == SelectionPointPosition.last:
            y2 += vector.y
            if y2 - y1 < min_size.height:
                y2 = y1 + min_size.height
        
        self.__box = Rectangle(x1, y1, x2 - x1, y2 - y1)
        
        # TODO: don't move current point
        self.__old_point = point
    
    def mouse_up(self, drawing_area, application):
        command = ResizeMoveElementCommand(
            self.__element,
            self.__box
        )
        application.commands.execute(command)
        self._finish()