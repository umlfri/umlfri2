from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ElementResizedMovedEvent as ElementResizedMovedEvent
from typing import Iterator
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.rectangle import Rectangle


class ResizeMoveElementCommand(Command):
    def __init__(
        self,
        element: ElementVisual,
        new_bounds: Rectangle
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ElementResizedMovedEvent]: ...
