from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionMovedEvent as ConnectionMovedEvent
from typing import Iterator
from umlfri2.application.events.diagram.connectionmoved import ConnectionMovedEvent
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.point import Point


class AddConnectionPointCommand(Command):
    def __init__(
        self,
        connection: ConnectionVisual,
        index: int,
        position: Point
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ConnectionMovedEvent]: ...
