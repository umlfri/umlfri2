from umlfri2.types.geometry import Rectangle
from .action import Action


class SelectManyAction(Action):
    __box = None
    
    @property
    def box(self):
        return self.__box
    
    def mouse_down(self, point):
        self.__box = Rectangle.from_point_point(point, point)
    
    def mouse_move(self, point):
        self.__box = Rectangle.from_point_point(self.__box.top_left, point)
    
    def mouse_up(self):
        self.drawing_area.selection.select_in_area(self.__box.normalize())
        self._finish()
