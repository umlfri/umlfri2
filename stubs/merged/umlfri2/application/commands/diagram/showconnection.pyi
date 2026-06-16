from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionShownEvent as ConnectionShownEvent
from umlfri2.types.geometry import Vector as Vector
from typing import Iterator
from umlfri2.application.events.diagram.connectionshown import ConnectionShownEvent
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ShowConnectionCommand(Command):
    def __init__(
        self,
        diagram: Diagram,
        connection_object: ConnectionObject
    ) -> None: ...
    @property
    def description(self): ...
    @property
    def connection_visual(self): ...
    @property
    def connection_object(self): ...
    def get_updates(self) -> Iterator[ConnectionShownEvent]: ...
