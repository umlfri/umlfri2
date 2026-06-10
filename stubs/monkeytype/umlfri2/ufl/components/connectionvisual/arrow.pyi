from typing import (
    List,
    Optional,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.types.color import Color
from umlfri2.types.enums.arroworientation import ArrowOrientation
from umlfri2.types.geometry.path import Path
from umlfri2.types.geometry.point import Point
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class ArrowDefinition:
    def __init__(
        self,
        id: str,
        path: Path,
        center: Point,
        rotation: float
    ) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def path(self) -> Path: ...


class ConnectionArrowComponent:
    def __init__(
        self,
        position: ConstantValueProvider,
        style: ConstantValueProvider,
        orientation: Optional[ConstantValueProvider] = ...,
        color: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...,
        fill: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...
    ) -> None: ...
    def _create_object(
        self,
        context: Context
    ) -> ConnectionArrowObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class ConnectionArrowObject:
    def __init__(
        self,
        position: float,
        style: ArrowDefinition,
        orientation: ArrowOrientation,
        color: Color,
        fill: Optional[Color]
    ) -> None: ...
    def assign_points(self, points: List[Point]) -> None: ...
    def draw(self, canvas: QTPainterCanvas) -> None: ...
