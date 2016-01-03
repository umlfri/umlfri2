from ..base import Event


class SelectionChangedEvent(Event):
    def __init__(self, diagram, selection):
        self.__diagram = diagram
        self.__selection = selection
    
    @property
    def diagram(self):
        return self.__diagram
    
    @property
    def selection(self):
        return self.__selection
    
    def get_opposite(self):
        return self
