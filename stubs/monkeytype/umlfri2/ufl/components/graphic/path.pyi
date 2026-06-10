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


class PathComponent:
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


class PathObject:
    def __init__(self, path: Path, fill: None, border: Color) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
