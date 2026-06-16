from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import ObjectDataChangedEvent as ObjectDataChangedEvent
from umlfri2.model import ElementObject as ElementObject
from umlfri2.ufl.objects.patch import UflObjectPatch as UflObjectPatch
from typing import (
    Iterator,
    Union,
)
from umlfri2.application.events.model.objectdatachanged import ObjectDataChangedEvent
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.ufl.objects.patch.object import UflObjectPatch


class ApplyPatchCommand(Command):
    def __init__(
        self,
        object: Union[ConnectionObject, ElementObject],
        patch: UflObjectPatch
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ObjectDataChangedEvent]: ...
