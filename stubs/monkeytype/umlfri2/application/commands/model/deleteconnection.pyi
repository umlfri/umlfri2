from typing import (
    Iterator,
    Union,
)
from umlfri2.application.events.diagram.connectionhidden import ConnectionHiddenEvent
from umlfri2.application.events.model.connectiondeleted import ConnectionDeletedEvent
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class DeleteConnectionCommand:
    def __init__(self, connection: ConnectionObject) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(
        self
    ) -> Iterator[Union[ConnectionDeletedEvent, ConnectionHiddenEvent]]: ...
