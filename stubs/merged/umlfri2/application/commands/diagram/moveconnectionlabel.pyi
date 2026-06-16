from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.commands.base import Command as Command
from umlfri2.application.events.diagram import ConnectionMovedEvent as ConnectionMovedEvent

class MoveConnectionLabelCommand(Command):
    def __init__(self, connection_label, delta) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
