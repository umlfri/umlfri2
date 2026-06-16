from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from umlfri2.types.geometry import Size as Size
from umlfri2.types.threestate import Maybe as Maybe
from umlfri2.ufl.types.basic import UflIntegerType as UflIntegerType
from umlfri2.ufl.types.structured import UflNullableType as UflNullableType
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

class SizerObject(VisualObject):
    def __init__(
        self,
        child: Any,
        minwidth: Optional[int],
        maxwidth: Optional[int],
        minheight: Optional[int],
        maxheight: Optional[int],
        width: Optional[int],
        height: Optional[int]
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(
        self
    ) -> Union[Tuple[MaybeType, MaybeType], Tuple[bool, bool]]: ...

class SizerComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    def __init__(
        self,
        children: List[Any],
        minwidth: Optional[ConstantValueProvider] = ...,
        maxwidth: Optional[ConstantValueProvider] = ...,
        minheight: Optional[ConstantValueProvider] = ...,
        maxheight: Optional[ConstantValueProvider] = ...,
        width: Optional[ConstantValueProvider] = ...,
        height: Optional[ConstantValueProvider] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
