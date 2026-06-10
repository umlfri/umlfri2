from typing import (
    Iterator,
    Tuple,
)
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.rectangle import Rectangle


class SnappedRectangle:
    def __init__(
        self,
        rectangle: Rectangle,
        horizontal_indicators: Tuple[()] = ...,
        vertical_indicators: Tuple[()] = ...
    ) -> None: ...
    @property
    def horizontal_indicators(self) -> Iterator[Point]: ...
    @property
    def rectangle(self) -> Rectangle: ...
    @property
    def vertical_indicators(self) -> Iterator[Point]: ...
