from umlfri2.application.commands.diagram import MoveSelectionCommand
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
    
    def mouse_down(self, drawing_area, application, point):
        self.__box = drawing_area.selection.get_bounds(application.ruler)
        self.__old_point = point
    
    def mouse_move(self, drawing_area, application, point):
        vector = point - self.__old_point
        self.__box += vector
        self.__old_point = point
    
    def mouse_up(self, drawing_area, application):
        old_bounds = drawing_area.selection.get_bounds(application.ruler)
        command = MoveSelectionCommand(
            drawing_area.selection,
            self.__box.top_left - old_bounds.top_left
        )
        application.commands.execute(command)
        self._finish()
