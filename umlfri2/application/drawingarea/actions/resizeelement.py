from umlfri2.application.commands.diagram import ResizeMoveElementCommand
from umlfri2.types.geometry import Rectangle
from ..selectionpointposition import SelectionPointPosition
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class ResizeElementAction(Action):
    __box = None
    __orig_box = None
    __old_point = None
    
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
            return DrawingAreaCursor.main_diagonal_resize
        elif self.__horizontal == SelectionPointPosition.center:
            return DrawingAreaCursor.vertical_resize
        elif self.__vertical == SelectionPointPosition.center:
            return DrawingAreaCursor.horizontal_resize
        else:
            return DrawingAreaCursor.anti_diagonal_resize
    
    def mouse_down(self, point):
        self.__orig_box = self.__box = self.drawing_area.selection.get_bounds()
        self.__old_point = point
    
    def mouse_move(self, point):
        x1 = self.__orig_box.x1
        y1 = self.__orig_box.y1
        x2 = self.__orig_box.x2
        y2 = self.__orig_box.y2
        
        vector = point - self.__old_point
        
        min_size = self.__element.get_minimal_size(self.application.ruler)
        
        if self.__horizontal == SelectionPointPosition.first:
            x1 += vector.x
            if x1 < 0:
                x1 = 0
            if x2 - x1 < min_size.width:
                x1 = x2 - min_size.width
        elif self.__horizontal == SelectionPointPosition.last:
            x2 += vector.x
            if x2 - x1 < min_size.width:
                x2 = x1 + min_size.width
        
        if self.__vertical == SelectionPointPosition.first:
            y1 += vector.y
            if y1 < 0:
                y1 = 0
            if y2 - y1 < min_size.height:
                y1 = y2 - min_size.height
        elif self.__vertical == SelectionPointPosition.last:
            y2 += vector.y
            if y2 - y1 < min_size.height:
                y2 = y1 + min_size.height
        
        self.__box = Rectangle(x1, y1, x2 - x1, y2 - y1)
    
    def mouse_up(self):
        command = ResizeMoveElementCommand(
            self.__element,
            self.__box
        )
        self.application.commands.execute(command)
        self._finish()
