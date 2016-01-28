from ..drawingareacursor import DrawingAreaCursor


class Action:
    def __init__(self):
        self.__finished = False
        self.__callback = None
        self.__application = None
        self.__drawing_area = None
    
    def _finish(self):
        self.__finished = True
        
        if self.__callback is not None:
            self.__callback()
    
    def associate(self, application, drawing_area):
        self.__application = application
        self.__drawing_area = drawing_area
    
    def snap_to(self, snapping):
        pass
    
    def after_finish(self, callback):
        self.__callback = callback
        return self
    
    @property
    def application(self):
        return self.__application
    
    @property
    def drawing_area(self):
        return self.__drawing_area
    
    @property
    def box(self):
        return None
    
    @property
    def path(self):
        return None
    
    @property
    def vertical_snapping_indicators(self):
        return ()
    
    @property
    def horizontal_snapping_indicators(self):
        return ()
    
    @property
    def finished(self):
        return self.__finished
    
    @property
    def cursor(self):
        return DrawingAreaCursor.arrow
    
    def mouse_down(self, point):
        pass
    
    def mouse_move(self, point):
        pass
    
    def mouse_up(self):
        self._finish()
