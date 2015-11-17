from ..base import Event


class ConnectionDeletedEvent(Event):
    def __init__(self, connection):
        self.__connection = connection
    
    @property
    def connection(self):
        return self.__connection
    
    def get_opposite(self):
        from .connectioncreated import ConnectionCreatedEvent
        
        return ConnectionCreatedEvent(self.__connection)
