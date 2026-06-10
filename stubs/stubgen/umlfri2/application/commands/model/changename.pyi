from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import ProjectChangedEvent as ProjectChangedEvent

class ChangeProjectNameCommand(Command):
    def __init__(self, project, name) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
