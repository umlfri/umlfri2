from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.commands.base import Command as Command
from umlfri2.application.events.diagram import ConnectionMovedEvent as ConnectionMovedEvent
from typing import Iterator
from umlfri2.application.events.diagram.connectionmoved import ConnectionMovedEvent
from umlfri2.model.connection.connectionlabel import ConnectionLabel
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.vector import Vector


class MoveConnectionLabelCommand(Command):
    def __init__(
        self,
        connection_label: ConnectionLabel,
        delta: Vector
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ConnectionMovedEvent]: ...
