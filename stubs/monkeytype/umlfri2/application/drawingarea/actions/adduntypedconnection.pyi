from typing import (
    Any,
    List,
    Optional,
)
from umlfri2.application.drawingarea.actions.action import ActionMenuItem
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.types.geometry.point import Point


class AddUntypedConnectionAction:
    def __init__(self, source_element: ElementVisual) -> None: ...
    def _create_connection(
        self,
        source_element: ElementVisual,
        destination_element: ElementVisual,
        points: List[Any]
    ) -> None: ...
    def _get_source_element(
        self,
        point: Point
    ) -> ElementVisual: ...
    @property
    def menu_to_show(self) -> Optional[List[ActionMenuItem]]: ...
