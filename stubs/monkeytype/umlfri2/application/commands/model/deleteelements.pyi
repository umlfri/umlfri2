from typing import (
    Iterator,
    Tuple,
    Union,
)
from umlfri2.application.events.diagram.connectionhidden import ConnectionHiddenEvent
from umlfri2.application.events.diagram.elementhidden import ElementHiddenEvent
from umlfri2.application.events.model.connectiondeleted import ConnectionDeletedEvent
from umlfri2.application.events.model.elementdeleted import ElementDeletedEvent
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class DeleteElementsCommand:
    def __init__(self, elements: Tuple[ElementObject]) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(
        self
    ) -> Iterator[Union[ElementDeletedEvent, ConnectionDeletedEvent, ElementHiddenEvent, ConnectionHiddenEvent]]: ...
