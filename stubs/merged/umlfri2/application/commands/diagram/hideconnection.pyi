from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionHiddenEvent as ConnectionHiddenEvent

class HideConnectionCommand(Command):
    def __init__(self, diagram, connection) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
