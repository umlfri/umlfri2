from ..base import Event


class ElementDeletedEvent(Event):
    def __init__(self, element, index=None):
        self.__element = element
        self.__index = index
    
    @property
    def element(self):
        return self.__element
    
    @property
    def index(self):
        return self.__index
    
    def get_opposite(self):
        from .elementcreated import ElementCreatedEvent
        
        return ElementCreatedEvent(self.__element, self.__index)
