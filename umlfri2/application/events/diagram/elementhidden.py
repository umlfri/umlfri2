from ..base import Event


class ElementHiddenEvent(Event):
    def __init__(self, element):
        self.__element = element
    
    @property
    def element(self):
        return self.__element
    
    def get_chained(self):
        from .diagramchanged import DiagramChangedEvent
        
        yield DiagramChangedEvent(self.__element.diagram)
    
    def get_opposite(self):
        from .elementshown import ElementShownEvent
        
        return ElementShownEvent(self.__element)
