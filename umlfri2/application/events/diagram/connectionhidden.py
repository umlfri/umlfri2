from ..base import Event


class ConnectionHiddenEvent(Event):
    def __init__(self, connection):
        self.__connection = connection
    
    @property
    def connection(self):
        return self.__connection
    
    def get_chained(self):
        from .diagramchanged import DiagramChangedEvent
        
        yield DiagramChangedEvent(self.__connection.diagram)
    
    def get_opposite(self):
        from .connectionshown import ConnectionShownEvent
        
        return ConnectionShownEvent(self.__connection)
