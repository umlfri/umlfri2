from typing import Iterator
from umlfri2.application.drawingarea.selection import Selection
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.vector import Vector


class MoveSelectionCommand:
    def __init__(
        self,
        selection: Selection,
        delta: Vector
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def _redo(self, ruler: QTRuler) -> None: ...
    def _undo(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ElementResizedMovedEvent]: ...
