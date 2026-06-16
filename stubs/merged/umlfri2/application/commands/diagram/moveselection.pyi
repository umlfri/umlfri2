from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent as ElementResizedMovedEvent
from typing import Iterator
from umlfri2.application.drawingarea.selection import Selection
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.vector import Vector


class MoveSelectionCommand(Command):
    def __init__(
        self,
        selection: Selection,
        delta: Vector
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ElementResizedMovedEvent]: ...
