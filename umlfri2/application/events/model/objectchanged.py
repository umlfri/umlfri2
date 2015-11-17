from ..base import Event


class ObjectChangedEvent(Event):
    def __init__(self, object, patch):
        self.__object = object
        self.__patch = patch
    
    @property
    def object(self):
        return self.__object
    
    @property
    def patch(self):
        return self.__patch
    
    def get_opposite(self):
        return ObjectChangedEvent(self.__object, self.__patch.make_reverse())
