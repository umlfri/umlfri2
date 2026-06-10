from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ElementResizedMovedEvent as ElementResizedMovedEvent

class ResizeMoveElementCommand(Command):
    def __init__(self, element, new_bounds) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
