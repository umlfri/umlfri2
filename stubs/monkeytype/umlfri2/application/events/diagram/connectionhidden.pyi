from typing import Iterator
from umlfri2.application.events.diagram.diagramchanged import DiagramChangedEvent
from umlfri2.model.connection.connectionvisual import ConnectionVisual


class ConnectionHiddenEvent:
    def __init__(self, connection: ConnectionVisual) -> None: ...
    def get_chained(self) -> Iterator[DiagramChangedEvent]: ...
