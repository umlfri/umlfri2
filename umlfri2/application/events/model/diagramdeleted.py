from ..base import Event


class DiagramDeletedEvent(Event):
    def __init__(self, diagram):
        self.__diagram = diagram
    
    @property
    def diagram(self):
        return self.__diagram
    
    def get_opposite(self):
        from .diagramcreated import DiagramCreatedEvent
        
        return DiagramCreatedEvent(self.__diagram)
