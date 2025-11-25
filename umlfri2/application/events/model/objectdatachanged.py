from __future__ import annotations

from typing import Any, TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.ufl.objects import UflObjectPatch


class ObjectDataChangedEvent(Event):
    def __init__(self, object: Any, patch: UflObjectPatch) -> None:
        self.__object = object
        self.__patch = patch
    
    @property
    def object(self) -> Any:
        return self.__object
    
    @property
    def patch(self) -> UflObjectPatch:
        return self.__patch
    
    def get_opposite(self) -> ObjectDataChangedEvent:
        return ObjectDataChangedEvent(self.__object, self.__patch.make_reverse())
