from umlfri2.application.commands.diagram import MoveSelectionCommand
from umlfri2.types.geometry import Vector
from ..drawingareacursor import DrawingAreaCursor
from .action import Action


class MoveSelectionAction(Action):
    def __init__(self):
        super().__init__()
        self.__old_box = None
        self.__box = None
        self.__snapping = None
        self.__snapped = None
    
    @property
    def cursor(self):
        return DrawingAreaCursor.move
    
    @property
    def box(self):
        return self.__box
    
    @property
    def horizontal_snapping_indicators(self):
        if self.__snapped is not None:
            yield from self.__snapped.horizontal_indicators
    
    @property
    def vertical_snapping_indicators(self):
        if self.__snapped is not None:
            yield from self.__snapped.vertical_indicators
    
    def snap_to(self, snapping):
        self.__snapping = snapping.ignore_selection().build()
    
    def mouse_down(self, point):
        box = self.drawing_area.selection.get_bounds()
        
        if self.__snapping is not None:
            self.__snapped = self.__snapping.snap_rectangle(box)
            self.__box = self.__snapped.rectangle
        else:
            self.__snapped = None
            self.__box = box
        
        self.__old_box = box
        self.__old_point = point
    
    def mouse_move(self, point):
        vector = point - self.__old_point
        box = self.__old_box + vector
        
        if box.x1 < 0:
            box -= Vector(box.x1, 0)
        if box.y1 < 0:
            box -= Vector(0, box.y1)
        
        if self.__snapping is not None:
            self.__snapped = self.__snapping.snap_rectangle(box)
            self.__box = self.__snapped.rectangle
        else:
            self.__snapped = None
            self.__box = box
    
    def mouse_up(self):
        old_bounds = self.drawing_area.selection.get_bounds()
        command = MoveSelectionCommand(
            self.drawing_area.selection,
            self.__box.top_left - old_bounds.top_left
        )
        self.application.commands.execute(command)
        self._finish()
