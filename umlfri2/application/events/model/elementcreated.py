from ..base import Event


class ElementCreatedEvent(Event):
    def __init__(self, element, index=None, indirect=False):
        self.__element = element
        self.__index = index
        self.__indirect = indirect
    
    @property
    def element(self):
        return self.__element
    
    @property
    def index(self):
        return self.__index
    
    @property
    def indirect(self):
        return self.__indirect
    
    def get_opposite(self):
        from .elementdeleted import ElementDeletedEvent
        
        return ElementDeletedEvent(self.__element, self.__index, self.__indirect)
