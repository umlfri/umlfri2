from typing import Iterator
from umlfri2.application.events.diagram.connectionmoved import ConnectionMovedEvent
from umlfri2.model.connection.connectionlabel import ConnectionLabel
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.vector import Vector


class MoveConnectionLabelCommand:
    def __init__(
        self,
        connection_label: ConnectionLabel,
        delta: Vector
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def _redo(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ConnectionMovedEvent]: ...
