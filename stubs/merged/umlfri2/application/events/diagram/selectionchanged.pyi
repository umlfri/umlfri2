from ..base import Event as Event
from umlfri2.application.drawingarea.selection import Selection
from umlfri2.model.diagram import Diagram


class SelectionChangedEvent(Event):
    def __init__(
        self,
        diagram: Diagram,
        selection: Selection
    ) -> None: ...
    @property
    def diagram(self) -> Diagram: ...
    @property
    def selection(self) -> Selection: ...
    def get_opposite(self): ...
