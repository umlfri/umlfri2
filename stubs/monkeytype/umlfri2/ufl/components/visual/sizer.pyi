from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.types.threestate import MaybeType
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class SizerComponent:
    def __init__(
        self,
        children: List[Any],
        minwidth: Optional[ConstantValueProvider] = ...,
        maxwidth: None = ...,
        minheight: Optional[ConstantValueProvider] = ...,
        maxheight: None = ...,
        width: Optional[ConstantValueProvider] = ...,
        height: Optional[ConstantValueProvider] = ...
    ) -> None: ...
    def _create_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> SizerObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class SizerObject:
    def __init__(
        self,
        child: Any,
        minwidth: Optional[int],
        maxwidth: None,
        minheight: Optional[int],
        maxheight: None,
        width: Optional[int],
        height: Optional[int]
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(
        self
    ) -> Union[Tuple[MaybeType, MaybeType], Tuple[bool, bool]]: ...
