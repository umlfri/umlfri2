from typing import Iterator
from umlfri2.application.events.diagram.diagramchanged import DiagramChangedEvent
from umlfri2.model.element.elementvisual import ElementVisual


class ElementShownEvent:
    def __init__(self, element: ElementVisual) -> None: ...
    def get_chained(self) -> Iterator[DiagramChangedEvent]: ...
