from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import ConnectionChangedEvent as ConnectionChangedEvent

class ReverseConnectionCommand(Command):
    def __init__(self, connection) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
