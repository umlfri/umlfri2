from typing import (
    Iterator,
    Optional,
)
from umlfri2.application.drawingarea.selection import Selection
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent
from umlfri2.qtgui.rendering.qtruler import QTRuler


class AlignSelectionCommand:
    def __init__(
        self,
        selection: Selection,
        vertical: None = ...,
        horizontal: Optional[AlignType] = ...
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def _redo(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ElementResizedMovedEvent]: ...
