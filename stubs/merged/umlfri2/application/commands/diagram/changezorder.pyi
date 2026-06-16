from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from enum import Enum
from umlfri2.application.events.diagram import ElementResizedMovedEvent as ElementResizedMovedEvent
from typing import (
    Iterator,
    Tuple,
)
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ZOrderDirection(Enum):
    bellow = 1
    above = 2
    bottom = 3
    top = 4

class ChangeZOrderCommand(Command):
    def __init__(
        self,
        diagram: Diagram,
        elements: Tuple[ElementVisual],
        direction: ZOrderDirection
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ElementResizedMovedEvent]: ...
