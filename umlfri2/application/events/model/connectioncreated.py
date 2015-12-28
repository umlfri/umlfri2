from ..base import Event


class ConnectionCreatedEvent(Event):
    def __init__(self, connection, indirect=False):
        self.__connection = connection
        self.__indirect = indirect
    
    @property
    def connection(self):
        return self.__connection
    
    @property
    def indirect(self):
        return self.__indirect
    
    def get_opposite(self):
        from .connectiondeleted import ConnectionDeletedEvent
        
        return ConnectionDeletedEvent(self.__connection, self.__indirect)
