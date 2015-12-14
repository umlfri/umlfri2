from umlfri2.application.commands.diagram import MoveSelectionCommand
from umlfri2.types.geometry import Vector
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveSelectionAction(Action):
    __box = None
    
    @property
    def cursor(self):
        return DrawingAreaCursor.move
    
    @property
    def box(self):
        return self.__box
    
    def mouse_down(self, point):
        self.__box = self.drawing_area.selection.get_bounds()
        self.__old_point = point
    
    def mouse_move(self, point):
        vector = point - self.__old_point
        self.__box += vector
        if self.__box.x1 < 0:
            self.__box -= Vector(self.__box.x1, 0)
        if self.__box.y1 < 0:
            self.__box -= Vector(0, self.__box.y1)
        self.__old_point = point
    
    def mouse_up(self):
        old_bounds = self.drawing_area.selection.get_bounds()
        command = MoveSelectionCommand(
            self.drawing_area.selection,
            self.__box.top_left - old_bounds.top_left
        )
        self.application.commands.execute(command)
        self._finish()
