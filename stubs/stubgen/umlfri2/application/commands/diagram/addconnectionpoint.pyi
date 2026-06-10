from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionMovedEvent as ConnectionMovedEvent

class AddConnectionPointCommand(Command):
    def __init__(self, connection, index, position) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
