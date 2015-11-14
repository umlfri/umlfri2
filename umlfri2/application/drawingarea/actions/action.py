from ..drawingareacursor import DrawingAreaCursor


class Action:
    def __init__(self):
        self.__finished = False
    
    def _finish(self):
        self.__finished = True
    
    @property
    def box(self):
        return None
    
    @property
    def path(self):
        return None
    
    @property
    def finished(self):
        return self.__finished
    
    @property
    def cursor(self):
        return DrawingAreaCursor.arrow
    
    def mouse_down(self, drawing_area, application, point):
        pass
    
    def mouse_move(self, drawing_area, application, point):
        pass
    
    def mouse_up(self, drawing_area, application):
        self._finish()
