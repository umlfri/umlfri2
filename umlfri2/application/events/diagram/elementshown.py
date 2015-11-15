from ..base import Event


class ElementShownEvent(Event):
    def __init__(self, element):
        self.__element = element
    
    @property
    def element(self):
        return self.__element
    
    def get_opposite(self):
        from .elementhidden import ElementHiddenEvent
        
        return ElementHiddenEvent(self.__element)
