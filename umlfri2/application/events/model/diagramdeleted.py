from ..base import Event


class DiagramDeletedEvent(Event):
    def __init__(self, diagram, index=None, indirect=False):
        self.__diagram = diagram
        self.__index = index
        self.__indirect = indirect
    
    @property
    def diagram(self):
        return self.__diagram
    
    @property
    def index(self):
        return self.__index
    
    @property
    def indirect(self):
        return self.__indirect
    
    def get_opposite(self):
        from .diagramcreated import DiagramCreatedEvent
        
        return DiagramCreatedEvent(self.__diagram, self.__index, self.__indirect)
