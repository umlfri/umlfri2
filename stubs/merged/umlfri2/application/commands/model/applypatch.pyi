from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import ObjectDataChangedEvent as ObjectDataChangedEvent
from umlfri2.model import ElementObject as ElementObject
from umlfri2.ufl.objects.patch import UflObjectPatch as UflObjectPatch

class ApplyPatchCommand(Command):
    def __init__(self, object, patch) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
