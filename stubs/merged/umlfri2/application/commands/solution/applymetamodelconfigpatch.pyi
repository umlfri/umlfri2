from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.solution import MetamodelConfigChangedEvent as MetamodelConfigChangedEvent

class ApplyMetamodelConfigPatchCommand(Command):
    def __init__(self, solution, project, patch) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
