from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Diagram
    from umlfri2.application.drawingarea.selection import Selection


class SelectionChangedEvent(Event):
    def __init__(self, diagram: Diagram, selection: Selection) -> None:
        self.__diagram = diagram
        self.__selection = selection
    
    @property
    def diagram(self) -> Diagram:
        return self.__diagram
    
    @property
    def selection(self) -> Selection:
        return self.__selection
    
    def get_opposite(self) -> SelectionChangedEvent:
        return self
