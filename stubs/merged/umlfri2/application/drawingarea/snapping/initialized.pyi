from .point import SnappedPoint as SnappedPoint
from .rectangle import SnappedRectangle as SnappedRectangle
from umlfri2.types.geometry import Point as Point, Vector as Vector
from typing import (
    Any,
    List,
    Union,
)
from umlfri2.application.drawingarea.snapping.point import SnappedPoint
from umlfri2.application.drawingarea.snapping.rectangle import SnappedRectangle
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.rectangle import Rectangle


class InitializedSnapping:
    MAXIMAL_DISTANCE: int
    def __init__(
        self,
        rectangles: List[Rectangle],
        points: List[Union[Any, Point]]
    ) -> None: ...
    def add_point(self, point: Point) -> None: ...
    def snap_point(
        self,
        point: Point
    ) -> SnappedPoint: ...
    def snap_rectangle(
        self,
        rectangle: Rectangle
    ) -> SnappedRectangle: ...
