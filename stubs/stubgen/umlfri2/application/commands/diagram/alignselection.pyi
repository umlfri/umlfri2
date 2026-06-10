from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from enum import Enum
from umlfri2.application.events.diagram import ElementResizedMovedEvent as ElementResizedMovedEvent
from umlfri2.types.geometry import Vector as Vector

class AlignType(Enum):
    minimum = 1
    center = 2
    maximum = 3

class AlignSelectionCommand(Command):
    def __init__(self, selection, vertical=None, horizontal=None) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
