from ..base.componenttype import ComponentType as ComponentType
from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .graphicalcomponent import GraphicalComponent as GraphicalComponent, GraphicalObject as GraphicalObject
from _typeshed import Incomplete
from umlfri2.types.geometry import PathBuilder as PathBuilder, Size as Size, Transformation as Transformation
from umlfri2.ufl.types.complex import UflColorType as UflColorType
from umlfri2.ufl.types.structured import UflNullableType as UflNullableType
from typing import (
    List,
    Optional,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.color import Color
from umlfri2.types.geometry.path import Path
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.ufl.components.pathpart.cubicto import CubicTo
from umlfri2.ufl.components.pathpart.moveto import MoveTo
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class PathObject(GraphicalObject):
    def __init__(self, path: Path, fill: None, border: Color) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...

class PathComponent(GraphicalComponent):
    ATTRIBUTES: Incomplete
    CHILDREN_TYPE: Incomplete
    def __init__(
        self,
        children: List[Union[MoveTo, CubicTo]],
        fill: None = ...,
        border: Optional[ConstantValueProvider] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def create_graphical_object(
        self,
        context: Context,
        ruler: QTRuler,
        size: Size
    ) -> PathObject: ...
