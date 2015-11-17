from ..base import Event


class ElementDeletedEvent(Event):
    def __init__(self, element):
        self.__element = element
    
    @property
    def element(self):
        return self.__element
    
    def get_opposite(self):
        from .elementcreated import ElementCreatedEvent
        
        return ElementCreatedEvent(self.__element)
