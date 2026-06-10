from typing import (
    Any,
    List,
    Union,
)
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.types.geometry.point import Point


class AddTypedConnectionAction:
    def __init__(self, type: str) -> None: ...
    def _create_connection(
        self,
        source_element: ElementVisual,
        destination_element: ElementVisual,
        points: List[Union[Any, Point]]
    ) -> None: ...
    def _get_source_element(
        self,
        point: Point
    ) -> ElementVisual: ...
