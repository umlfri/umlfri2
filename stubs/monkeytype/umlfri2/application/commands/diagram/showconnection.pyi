from typing import Iterator
from umlfri2.application.events.diagram.connectionshown import ConnectionShownEvent
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ShowConnectionCommand:
    def __init__(
        self,
        diagram: Diagram,
        connection_object: ConnectionObject
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ConnectionShownEvent]: ...
