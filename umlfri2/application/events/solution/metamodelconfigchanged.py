from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.metamodel import Metamodel
    from umlfri2.ufl.objects import UflObjectPatch


class MetamodelConfigChangedEvent(Event):
    def __init__(self, metamodel: Metamodel, patch: UflObjectPatch) -> None:
        self.__metamodel = metamodel
        self.__patch = patch

    @property
    def metamodel(self) -> Metamodel:
        return self.__metamodel

    @property
    def patch(self) -> UflObjectPatch:
        return self.__patch

    def get_opposite(self) -> MetamodelConfigChangedEvent:
        return MetamodelConfigChangedEvent(self.__metamodel, self.__patch.make_reverse())
