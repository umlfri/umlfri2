from typing import (
    Iterator,
    Set,
    Tuple,
    Union,
)
from umlfri2.types.geometry.point import Point


class SnappedPoint:
    def __init__(
        self,
        point: Point,
        horizontal_indicators: Union[Tuple[()], Set[Point]] = ...,
        vertical_indicators: Union[Tuple[()], Set[Point]] = ...
    ) -> None: ...
    @property
    def horizontal_indicators(self) -> Iterator[Point]: ...
    @property
    def point(self) -> Point: ...
    @property
    def snapped_horizontally(self) -> bool: ...
    @property
    def snapped_vertically(self) -> bool: ...
    @property
    def vertical_indicators(self) -> Iterator[Point]: ...
