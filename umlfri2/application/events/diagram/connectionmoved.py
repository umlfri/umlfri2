from ..base import Event


class ConnectionMovedEvent(Event):
    def __init__(self, connection):
        self.__connection = connection
    
    @property
    def connection(self):
        return self.__connection
    
    def get_opposite(self):
        return self
