from __future__ import annotations

from typing import TYPE_CHECKING, Union

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.ufl.objects import UflObjectPatch
    from umlfri2.model import ElementObject, ConnectionObject, Diagram


class ObjectDataChangedEvent(Event):
    def __init__(self, object: Union[ElementObject, ConnectionObject, Diagram], patch: UflObjectPatch) -> None:
        self.__object = object
        self.__patch = patch
    
    @property
    def object(self) -> Union[ElementObject, ConnectionObject, Diagram]:
        return self.__object
    
    @property
    def patch(self) -> UflObjectPatch:
        return self.__patch
    
    def get_opposite(self) -> ObjectDataChangedEvent:
        return ObjectDataChangedEvent(self.__object, self.__patch.make_reverse())
