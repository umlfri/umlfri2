from ..base import Event


class ItemSelectedEvent(Event):
    """
    Item selected in the project tree.
    """
    
    def __init__(self, item):
        self.__item = item
    
    @property
    def item(self):
        return self.__item
