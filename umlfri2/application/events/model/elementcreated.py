from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import ElementObject


class ElementCreatedEvent(Event):
    def __init__(self, element: ElementObject, index: Optional[int] = None, indirect: bool = False) -> None:
        self.__element = element
        self.__index = index
        self.__indirect = indirect
    
    @property
    def element(self) -> ElementObject:
        return self.__element
    
    @property
    def index(self) -> Optional[int]:
        return self.__index
    
    @property
    def indirect(self) -> bool:
        return self.__indirect
    
    def get_opposite(self) -> ElementDeletedEvent:
        from .elementdeleted import ElementDeletedEvent
        
        return ElementDeletedEvent(self.__element, self.__index, self.__indirect)
