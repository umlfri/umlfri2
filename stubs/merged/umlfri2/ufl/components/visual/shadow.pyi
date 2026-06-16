from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from typing import NamedTuple
from umlfri2.types.color import Colors as Colors
from umlfri2.types.geometry import Vector as Vector
from umlfri2.ufl.types.basic import UflIntegerType as UflIntegerType
from umlfri2.ufl.types.complex import UflColorType as UflColorType
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
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.components.visual.diamond import (
    DiamondComponent,
    DiamondObject,
)
from umlfri2.ufl.components.visual.rectangle import (
    RectangleComponent,
    RectangleObject,
    RoundedRectangleObject,
)
from umlfri2.ufl.components.visual.vbox import VBoxComponent
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class ShadowInfo(NamedTuple):
    color: Incomplete
    shift: Incomplete

class ShadowObject(VisualObject):
    def __init__(
        self,
        child: Union[RectangleObject, DiamondObject, RoundedRectangleObject],
        color: Color,
        padding: int
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...

class ShadowComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    def __init__(
        self,
        children: List[Union[VBoxComponent, DiamondComponent, RectangleComponent]],
        color: Optional[DynamicValueProvider] = ...,
        padding: Optional[ConstantValueProvider] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
