from typing import (
    Iterator,
    Tuple,
)
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ChangeZOrderCommand:
    def __init__(
        self,
        diagram: Diagram,
        elements: Tuple[ElementVisual],
        direction: ZOrderDirection
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def _redo(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ElementResizedMovedEvent]: ...
