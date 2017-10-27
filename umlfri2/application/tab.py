from .drawingarea import DrawingArea


class Tab:
    def __init__(self, application, tabs, diagram, locked=False):
        self.__tabs = tabs
        self.__drawing_area = DrawingArea(application, diagram)
        self.__locked = locked
    
    @property
    def locked(self):
        return self.__locked
    
    def lock(self):
        self.__locked = True
    
    def unlock(self):
        self.__locked = False
    
    def close(self):
        self.__tabs._close_tab(self)
    
    @property
    def drawing_area(self):
        return self.__drawing_area
    
    @property
    def name(self):
        return self.__drawing_area.diagram.get_display_name()
    
    @property
    def icon(self):
        return self.__drawing_area.diagram.type.icon
