from ..base import Event


class ConnectionCreatedEvent(Event):
    def __init__(self, connection):
        self.__connection = connection
    
    @property
    def connection(self):
        return self.__connection
    
    def get_opposite(self):
        from .connectiondeleted import ConnectionDeletedEvent
        
        return ConnectionDeletedEvent(self.__connection)
