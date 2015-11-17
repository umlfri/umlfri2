from ..base import Event


class ElementCreatedEvent(Event):
    def __init__(self, element):
        self.__element = element
    
    @property
    def element(self):
        return self.__element
    
    def get_opposite(self):
        from .elementdeleted import ElementDeletedEvent
        
        return ElementDeletedEvent(self.__element)
