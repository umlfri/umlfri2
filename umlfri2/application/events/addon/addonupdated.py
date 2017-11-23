from ..base import Event


class AddOnUpdatedEvent(Event):
    def __init__(self, addon):
        self.__addon = addon
    
    @property
    def addon(self):
        return self.__addon
