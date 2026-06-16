from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .hbox import HBoxComponent as HBoxComponent
from .table import TableColumn as TableColumn, TableRow as TableRow
from .vbox import VBoxComponent as VBoxComponent
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import LineOrientation as LineOrientation
from umlfri2.types.geometry import Size as Size
from umlfri2.types.threestate import Maybe as Maybe
from umlfri2.ufl.types.complex import UflColorType as UflColorType
from umlfri2.ufl.types.enum import UflTypedEnumType as UflTypedEnumType
from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.color import Color
from umlfri2.types.enums.lineorientation import LineOrientation
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.types.threestate import MaybeType
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class LineObject(VisualObject):
    def __init__(
        self,
        orientation: LineOrientation,
        color: Color
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(self) -> Tuple[MaybeType, bool]: ...

class LineComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    def __init__(
        self,
        orientation: Optional[ConstantValueProvider] = ...,
        color: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
