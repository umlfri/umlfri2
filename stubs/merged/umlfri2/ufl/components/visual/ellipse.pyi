from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from umlfri2.types.geometry import Rectangle as Rectangle, Size as Size
from umlfri2.types.threestate import Maybe as Maybe
from umlfri2.ufl.types.complex import UflColorType as UflColorType
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

class EllipseObject(VisualObject):
    def __init__(
        self,
        child: Optional[PaddingObject],
        fill: Color,
        border: Optional[Color]
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...

class EllipseComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    def __init__(
        self,
        children: List[Union[Any, PaddingComponent]],
        fill: Optional[Union[ConstantValueProvider, DynamicValueProvider]] = ...,
        border: Optional[Union[ConstantValueProvider, DynamicValueProvider]] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
