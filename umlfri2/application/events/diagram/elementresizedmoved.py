from umlfri2.application.events.base import Event


class ElementResizedMovedEvent(Event):
    def __init__(self, element):
        self.__element = element
    
    @property
    def element(self):
        return self.__element
    
    def get_chained(self):
        from .diagramchanged import DiagramChangedEvent
        
        yield DiagramChangedEvent(self.__element.diagram)
    
    def get_opposite(self):
        return self
