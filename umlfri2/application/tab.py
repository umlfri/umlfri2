from .drawingarea import DrawingArea


class Tab:
    def __init__(self, application, diagram):
        self.__drawing_area = DrawingArea(application, diagram)
        self.__is_current = False
    
    @property
    def is_current(self):
        return self.__is_current
    
    @is_current.setter
    def is_current(self, value):
        self.__is_current = value
        
        if not value:
            self.__drawing_area.switched_to_background()
    
    @property
    def drawing_area(self):
        return self.__drawing_area
    
    @property
    def diagram_type(self):
        return self.__drawing_area.diagram.type
    
    @property
    def name(self):
        return self.__drawing_area.diagram.get_display_name()
    
    @property
    def icon(self):
        return self.__drawing_area.diagram.type.icon
