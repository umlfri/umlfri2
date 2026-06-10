from typing import Iterator
from umlfri2.application.events.diagram.connectionmoved import ConnectionMovedEvent
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.vector import Vector


class MoveConnectionPointCommand:
    def __init__(
        self,
        connection: ConnectionVisual,
        index: int,
        delta: Vector
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def _redo(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ConnectionMovedEvent]: ...
