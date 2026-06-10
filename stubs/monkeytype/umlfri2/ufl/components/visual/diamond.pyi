from typing import (
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
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.components.visual.padding import (
    PaddingComponent,
    PaddingObject,
)
from umlfri2.ufl.components.visual.shadow import ShadowInfo
from umlfri2.ufl.components.visual.sizer import (
    SizerComponent,
    SizerObject,
)
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class DiamondComponent:
    def __init__(
        self,
        children: List[Union[SizerComponent, PaddingComponent]],
        fill: Optional[DynamicValueProvider] = ...,
        border: Optional[DynamicValueProvider] = ...
    ) -> None: ...
    def _create_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> DiamondObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class DiamondObject:
    def __init__(
        self,
        child: Union[PaddingObject, SizerObject],
        fill: Color,
        border: Color
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(
        self,
        canvas: QTPainterCanvas,
        shadow: Optional[ShadowInfo]
    ) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...
