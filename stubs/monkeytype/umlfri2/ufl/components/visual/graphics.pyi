from typing import (
    List,
    Tuple,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.ufl.components.graphic.path import (
    PathComponent,
    PathObject,
)
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class GraphicsComponent:
    def __init__(
        self,
        children: List[PathComponent],
        width: ConstantValueProvider,
        height: ConstantValueProvider
    ) -> None: ...
    def _create_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> GraphicsObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class GraphicsObject:
    def __init__(self, children: List[PathObject]) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...
