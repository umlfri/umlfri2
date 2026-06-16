from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from enum import Enum
from umlfri2.application.events.diagram import ElementResizedMovedEvent as ElementResizedMovedEvent
from umlfri2.types.geometry import Vector as Vector
from typing import (
    Iterator,
    Optional,
)
from umlfri2.application.drawingarea.selection import Selection
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent
from umlfri2.qtgui.rendering.qtruler import QTRuler


class AlignType(Enum):
    minimum = 1
    center = 2
    maximum = 3

class AlignSelectionCommand(Command):
    def __init__(
        self,
        selection: Selection,
        vertical: None = None,
        horizontal: Optional[AlignType] = None
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ElementResizedMovedEvent]: ...
