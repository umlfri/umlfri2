from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .connectionvisualcomponent import ConnectionVisualComponent as ConnectionVisualComponent, ConnectionVisualObject as ConnectionVisualObject
from _typeshed import Incomplete
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import LineStyle as LineStyle
from umlfri2.types.geometry import PathBuilder as PathBuilder
from umlfri2.types.proportion import EMPTY_PROPORTION as EMPTY_PROPORTION, WHOLE_PROPORTION as WHOLE_PROPORTION
from umlfri2.ufl.types.complex import UflColorType as UflColorType, UflProportionType as UflProportionType
from umlfri2.ufl.types.enum import UflTypedEnumType as UflTypedEnumType
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

class ConnectionLineObject(ConnectionVisualObject):
    def __init__(
        self,
        start: float,
        end: float,
        style: LineStyle,
        color: Color
    ) -> None: ...
    def assign_points(self, points: List[Point]) -> None: ...
    def draw(self, canvas: QTPainterCanvas) -> None: ...

class ConnectionLineComponent(ConnectionVisualComponent):
    ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    def __init__(
        self,
        start: Optional[ConstantValueProvider] = ...,
        end: Optional[ConstantValueProvider] = ...,
        style: Optional[ConstantValueProvider] = ...,
        color: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
