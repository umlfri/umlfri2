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


class AddDiagramElementCommand:
    def __init__(
        self,
        diagram: Diagram,
        element_type: ElementType,
        point: Point
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    @property
    def element_visual(self) -> ElementVisual: ...
    def get_updates(
        self
    ) -> Iterator[Union[ElementCreatedEvent, ElementShownEvent]]: ...
