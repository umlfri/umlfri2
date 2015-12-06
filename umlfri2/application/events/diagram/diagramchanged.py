from ..base import Event


class DiagramChangedEvent(Event):
    def __init__(self, diagram):
        self.__diagram = diagram
    
    @property
    def diagram(self):
        return self.__diagram
    
    def get_opposite(self):
        return self
