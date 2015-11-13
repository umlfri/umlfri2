from .selection import Selection


class Tab:
    def __init__(self, diagram):
        self.__diagram = diagram
        self.__selection = Selection(self.__diagram)
    
    @property
    def diagram(self):
        return self.__diagram
    
    @property
    def selection(self):
        return self.__selection
    
    def draw(self, canvas):
        self.__diagram.draw(canvas, self.__selection)
    
    @property
    def name(self):
        return self.__diagram.get_display_name()
    
    @property
    def icon(self):
        return self.__diagram.type.icon
