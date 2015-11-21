from ..base import Event


class ClosedTabEvent(Event):
    def __init__(self, tab):
        self.__tab = tab
    
    @property
    def tab(self):
        return self.__tab
