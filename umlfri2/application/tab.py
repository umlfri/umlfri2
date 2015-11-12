class Tab:
    def __init__(self, diagram):
        self.__diagram = diagram
    
    @property
    def diagram(self):
        return self.__diagram
    
    def draw(self, canvas):
        self.__diagram.draw(canvas)
    
    @property
    def name(self):
        return self.__diagram.get_display_name()
