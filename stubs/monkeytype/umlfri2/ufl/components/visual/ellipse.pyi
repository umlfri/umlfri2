from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.color import Color
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.components.visual.padding import (
    PaddingComponent,
    PaddingObject,
)
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class EllipseComponent:
    def __init__(
        self,
        children: List[Union[Any, PaddingComponent]],
        fill: Optional[Union[ConstantValueProvider, DynamicValueProvider]] = ...,
        border: Optional[Union[ConstantValueProvider, DynamicValueProvider]] = ...
    ) -> None: ...
    def _create_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> EllipseObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class EllipseObject:
    def __init__(
        self,
        child: Optional[PaddingObject],
        fill: Color,
        border: Optional[Color]
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...
