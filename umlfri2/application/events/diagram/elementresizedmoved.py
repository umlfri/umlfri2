from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from umlfri2.application.events.base import Event

if TYPE_CHECKING:
    from umlfri2.model.element import ElementVisual


class ElementResizedMovedEvent(Event):
    def __init__(self, element: ElementVisual) -> None:
        self.__element = element
    
    @property
    def element(self) -> ElementVisual:
        return self.__element
    
    def get_chained(self) -> Iterator[Event]:
        from .diagramchanged import DiagramChangedEvent
        
        yield DiagramChangedEvent(self.__element.diagram)
    
    def get_opposite(self) -> ElementResizedMovedEvent:
        return self
