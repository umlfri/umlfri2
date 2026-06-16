from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionHiddenEvent as ConnectionHiddenEvent
from typing import Iterator
from umlfri2.application.events.diagram.connectionhidden import ConnectionHiddenEvent
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.rendering.qtruler import QTRuler


class HideConnectionCommand(Command):
    def __init__(
        self,
        diagram: Diagram,
        connection: ConnectionVisual
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ConnectionHiddenEvent]: ...
