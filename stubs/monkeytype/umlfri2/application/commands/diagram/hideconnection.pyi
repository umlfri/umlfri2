from typing import Iterator
from umlfri2.application.events.diagram.connectionhidden import ConnectionHiddenEvent
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.rendering.qtruler import QTRuler


class HideConnectionCommand:
    def __init__(
        self,
        diagram: Diagram,
        connection: ConnectionVisual
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def _redo(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ConnectionHiddenEvent]: ...
