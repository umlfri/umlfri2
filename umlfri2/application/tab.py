from .drawingarea import DrawingArea


class Tab:
    def __init__(self, application, diagram):
        self.__drawing_area = DrawingArea(application, diagram)
    
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
