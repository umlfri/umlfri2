from umlfri2.types.geometry import Rectangle
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class SelectManyAction(Action):
    __box = None
    
    @property
    def box(self):
        return self.__box
    
    def mouse_down(self, drawing_area, application, point):
        self.__box = Rectangle.from_point_point(point, point)
    
    def mouse_move(self, drawing_area, application, point):
        self.__box = Rectangle.from_point_point(self.__box.top_left, point)
    
    def mouse_up(self, drawing_area, application):
        drawing_area.selection.select_in_area(application.ruler, self.__box.normalize())
        self._finish()
