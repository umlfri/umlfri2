from typing import Iterator
from umlfri2.application.events.model.connectionchanged import ConnectionChangedEvent
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ReverseConnectionCommand:
    def __init__(self, connection: ConnectionObject) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ConnectionChangedEvent]: ...
