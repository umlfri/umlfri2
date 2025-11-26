from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.drawingarea import DrawingArea


class ZoomChangedEvent(Event):
    def __init__(self, drawing_area: DrawingArea) -> None:
        self.__drawing_area = drawing_area
    
    @property
    def drawing_area(self) -> DrawingArea:
        return self.__drawing_area
