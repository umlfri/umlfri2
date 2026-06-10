from typing import Iterator
from umlfri2.application.events.model.nodemoved import NodeMovedEvent
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class MoveNodeCommand:
    def __init__(
        self,
        node: ElementObject,
        new_parent: ElementObject,
        new_index: int
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[NodeMovedEvent]: ...
