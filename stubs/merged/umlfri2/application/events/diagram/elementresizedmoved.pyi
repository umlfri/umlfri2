from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.base import Event as Event
from typing import Iterator
from umlfri2.application.events.diagram.diagramchanged import DiagramChangedEvent
from umlfri2.model.element.elementvisual import ElementVisual


class ElementResizedMovedEvent(Event):
    def __init__(self, element: ElementVisual) -> None: ...
    @property
    def element(self): ...
    def get_chained(self) -> Iterator[DiagramChangedEvent]: ...
    def get_opposite(self) -> ElementResizedMovedEvent: ...
