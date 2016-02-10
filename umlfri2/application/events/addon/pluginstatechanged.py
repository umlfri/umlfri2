from ..base import Event


class PluginStateChangedEvent(Event):
    def __init__(self, addon, state):
        self.__addon = addon
        self.__state = state
    
    @property
    def addon(self):
        return self.__addon
    
    @property
    def addon_state(self):
        return self.__state
