from __future__ import annotations

from ..base import Event


class ZoomChangedEvent(Event):
    def __init__(self, drawing_area: object) -> None:
        self.__drawing_area = drawing_area
    
    @property
    def drawing_area(self) -> object:
        return self.__drawing_area
