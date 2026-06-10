from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from enum import Enum
from umlfri2.application.events.diagram import ElementResizedMovedEvent as ElementResizedMovedEvent

class ZOrderDirection(Enum):
    bellow = 1
    above = 2
    bottom = 3
    top = 4

class ChangeZOrderCommand(Command):
    def __init__(self, diagram, elements, direction) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
