from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ElementShownEvent as ElementShownEvent
from umlfri2.application.events.model import ElementCreatedEvent as ElementCreatedEvent
from typing import (
    Iterator,
    Union,
)
from umlfri2.application.events.diagram.elementshown import ElementShownEvent
from umlfri2.application.events.model.elementcreated import ElementCreatedEvent
from umlfri2.metamodel.elementtype import ElementType
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.point import Point


class AddDiagramElementCommand(Command):
    def __init__(
        self,
        diagram: Diagram,
        element_type: ElementType,
        point: Point
    ) -> None: ...
    @property
    def description(self): ...
    @property
    def element_visual(self) -> ElementVisual: ...
    @property
    def element_object(self): ...
    def get_updates(
        self
    ) -> Iterator[Union[ElementCreatedEvent, ElementShownEvent]]: ...
