from ..base import Event as Event
from _typeshed import Incomplete
from collections.abc import Generator
from typing import Iterator
from umlfri2.application.events.diagram.diagramchanged import DiagramChangedEvent
from umlfri2.model.element.elementvisual import ElementVisual


class ElementShownEvent(Event):
    def __init__(self, element: ElementVisual) -> None: ...
    @property
    def element(self): ...
    def get_chained(self) -> Iterator[DiagramChangedEvent]: ...
    def get_opposite(self): ...
