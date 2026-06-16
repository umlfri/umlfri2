from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .connectionvisualcomponent import ConnectionVisualComponent as ConnectionVisualComponent, ConnectionVisualObject as ConnectionVisualObject
from _typeshed import Incomplete
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import ArrowOrientation as ArrowOrientation
from umlfri2.types.geometry import Transformation as Transformation
from umlfri2.ufl.types.complex import UflColorType as UflColorType, UflProportionType as UflProportionType
from umlfri2.ufl.types.enum import UflDefinedEnumType as UflDefinedEnumType, UflTypedEnumType as UflTypedEnumType
from umlfri2.ufl.types.structured import UflNullableType as UflNullableType
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

class ConnectionArrowObject(ConnectionVisualObject):
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

class ConnectionArrowComponent(ConnectionVisualComponent):
    ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    def __init__(
        self,
        position: ConstantValueProvider,
        style: ConstantValueProvider,
        orientation: Optional[ConstantValueProvider] = ...,
        color: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...,
        fill: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
