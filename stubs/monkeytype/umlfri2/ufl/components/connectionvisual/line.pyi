from typing import (
    List,
    Optional,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.types.color import Color
from umlfri2.types.enums.linestyle import LineStyle
from umlfri2.types.geometry.point import Point
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class ConnectionLineComponent:
    def __init__(
        self,
        start: Optional[ConstantValueProvider] = ...,
        end: Optional[ConstantValueProvider] = ...,
        style: Optional[ConstantValueProvider] = ...,
        color: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...
    ) -> None: ...
    def _create_object(
        self,
        context: Context
    ) -> ConnectionLineObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class ConnectionLineObject:
    def __init__(
        self,
        start: float,
        end: float,
        style: LineStyle,
        color: Color
    ) -> None: ...
    def assign_points(self, points: List[Point]) -> None: ...
    def draw(self, canvas: QTPainterCanvas) -> None: ...
