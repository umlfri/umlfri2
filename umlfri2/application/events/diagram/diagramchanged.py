from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Diagram


class DiagramChangedEvent(Event):
    def __init__(self, diagram: Diagram) -> None:
        self.__diagram = diagram
    
    @property
    def diagram(self) -> Diagram:
        return self.__diagram
    
    def get_opposite(self) -> DiagramChangedEvent:
        return self
