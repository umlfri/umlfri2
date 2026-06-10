from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import NodeMovedEvent as NodeMovedEvent

class MoveNodeCommand(Command):
    def __init__(self, node, new_parent, new_index) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
