from ..base import Event


class DiagramCreatedEvent(Event):
    def __init__(self, diagram):
        self.__diagram = diagram
    
    @property
    def diagram(self):
        return self.__diagram
    
    def get_opposite(self):
        from .diagramdeleted import DiagramDeletedEvent
        
        return DiagramDeletedEvent(self.__diagram)
