from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram.elementresizedmoved import ElementResizedMovedEvent as ElementResizedMovedEvent

class MoveSelectionCommand(Command):
    def __init__(self, selection, delta) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
