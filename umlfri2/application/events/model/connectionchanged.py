from ..base import Event


class ConnectionChangedEvent(Event):
    def __init__(self, connection):
        self.__connection = connection
    
    @property
    def connection(self):
        return self.__connection
    
    def get_opposite(self):
        return ConnectionChangedEvent(self.__connection)
