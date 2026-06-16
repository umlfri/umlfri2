from ..base import Event as Event
from umlfri2.application.drawingarea.drawingarea import DrawingArea


class ZoomChangedEvent(Event):
    def __init__(self, drawing_area: DrawingArea) -> None: ...
    @property
    def drawing_area(self): ...
