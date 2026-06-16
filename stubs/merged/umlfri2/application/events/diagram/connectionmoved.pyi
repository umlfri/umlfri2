from ..base import Event as Event
from _typeshed import Incomplete
from collections.abc import Generator
from typing import Iterator
from umlfri2.application.events.diagram.diagramchanged import DiagramChangedEvent
from umlfri2.model.connection.connectionvisual import ConnectionVisual


class ConnectionMovedEvent(Event):
    def __init__(self, connection: ConnectionVisual) -> None: ...
    @property
    def connection(self): ...
    def get_chained(self) -> Iterator[DiagramChangedEvent]: ...
    def get_opposite(self): ...
