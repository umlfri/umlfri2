from umlfri2.model.connection.connectionobject import ConnectionObject


class ConnectionDeletedEvent:
    def __init__(
        self,
        connection: ConnectionObject,
        indirect: bool = ...
    ) -> None: ...
    @property
    def connection(self) -> ConnectionObject: ...
