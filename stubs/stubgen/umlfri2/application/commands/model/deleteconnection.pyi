from ..base import Command as Command
from ..diagram import HideConnectionCommand as HideConnectionCommand
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import ConnectionDeletedEvent as ConnectionDeletedEvent

class DeleteConnectionCommand(Command):
    def __init__(self, connection) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete, Incomplete]: ...
