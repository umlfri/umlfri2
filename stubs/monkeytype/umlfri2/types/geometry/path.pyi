from typing import (
    Any,
    List,
    Tuple,
    Union,
)
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.transformation import Transformation


class Path:
    def __init__(self, segments: List[Union[Any, PathSegment]]) -> None: ...
    @property
    def segments(
        self
    ) -> Union[Tuple[PathSegment, PathSegment], Tuple[()], Tuple[PathSegment]]: ...
    def transform(
        self,
        matrix: Transformation
    ) -> Path: ...


class PathBuilder:
    def __init__(self) -> None: ...
    def build(self) -> Path: ...
    def close(self) -> PathBuilder: ...
    def cubic_to(
        self,
        control1: Point,
        control2: Point,
        point: Point
    ) -> PathBuilder: ...
    def from_path(
        self,
        path: Path,
        join_moves: bool = ...
    ) -> PathBuilder: ...
    def from_string(self, s: str) -> PathBuilder: ...
    def line_to(self, point: Point) -> PathBuilder: ...
    def move_or_line_to(self, point: Point) -> None: ...
    def move_to(self, point: Point) -> PathBuilder: ...


class PathCommand:
    def __init__(self, final_point: Point) -> None: ...
    @property
    def final_point(self) -> Point: ...


class PathCubicTo:
    def __init__(
        self,
        control_point1: Point,
        control_point2: Point,
        final_point: Point
    ) -> None: ...
    @property
    def control_point1(self) -> Point: ...
    @property
    def control_point2(self) -> Point: ...
    def transform(
        self,
        matrix: Transformation
    ) -> PathCubicTo: ...


class PathLineTo:
    def transform(
        self,
        matrix: Transformation
    ) -> PathLineTo: ...


class PathSegment:
    def __init__(
        self,
        starting_point: Point,
        commands: List[Union[PathCubicTo, PathLineTo]],
        closed: bool = ...
    ) -> None: ...
    @property
    def closed(self) -> bool: ...
    @property
    def commands(self) -> Any: ...
    @property
    def starting_point(self) -> Point: ...
    def transform(
        self,
        matrix: Transformation
    ) -> PathSegment: ...
