from umlfri2.model.connection.connectionobject import ConnectionObject


class ConnectionCreatedEvent:
    def __init__(
        self,
        connection: ConnectionObject,
        indirect: bool = ...
    ) -> None: ...
