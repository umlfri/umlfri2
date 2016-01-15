from ..base import Event


class PluginStartedEvent(Event):
    def __init__(self, addon):
        self.__addon = addon
    
    @property
    def addon(self):
        return self.__addon
