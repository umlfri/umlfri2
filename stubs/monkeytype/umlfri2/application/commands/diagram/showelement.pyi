from typing import Iterator
from umlfri2.application.events.diagram.elementshown import ElementShownEvent
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.point import Point


class ShowElementCommand:
    def __init__(
        self,
        diagram: Diagram,
        element_object: ElementObject,
        point: Point
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ElementShownEvent]: ...
