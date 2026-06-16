from ..base import Event as Event
from umlfri2.model.connection.connectionobject import ConnectionObject


class ConnectionDeletedEvent(Event):
    def __init__(
        self,
        connection: ConnectionObject,
        indirect: bool = False
    ) -> None: ...
    @property
    def connection(self) -> ConnectionObject: ...
    @property
    def indirect(self): ...
    def get_opposite(self): ...
