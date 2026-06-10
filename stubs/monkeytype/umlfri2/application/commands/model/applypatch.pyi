from typing import (
    Iterator,
    Union,
)
from umlfri2.application.events.model.objectdatachanged import ObjectDataChangedEvent
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.ufl.objects.patch.object import UflObjectPatch


class ApplyPatchCommand:
    def __init__(
        self,
        object: Union[ConnectionObject, ElementObject],
        patch: UflObjectPatch
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ObjectDataChangedEvent]: ...
