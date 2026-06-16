from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from umlfri2.types.enums import HorizontalAlignment as HorizontalAlignment, VerticalAlignment as VerticalAlignment
from umlfri2.types.geometry import Rectangle as Rectangle
from umlfri2.types.threestate import Maybe as Maybe
from umlfri2.ufl.types.enum import UflTypedEnumType as UflTypedEnumType
from umlfri2.ufl.types.structured import UflNullableType as UflNullableType
from typing import (
    List,
    Optional,
    Tuple,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.enums.alignment import (
    HorizontalAlignment,
    VerticalAlignment,
)
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.types.threestate import MaybeType
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.visual.line import LineObject
from umlfri2.ufl.components.visual.rectangle import RectangleObject
from umlfri2.ufl.components.visual.sizer import SizerObject
from umlfri2.ufl.components.visual.textbox import TextBoxObject
from umlfri2.ufl.components.visual.vbox import VBoxObject
from umlfri2.ufl.components.visual.visualcomponent import VisualComponent
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class AlignObject(VisualObject):
    def __init__(
        self,
        child: Union[LineObject, VBoxObject, SizerObject, TextBoxObject, RectangleObject],
        horizontal: Optional[HorizontalAlignment],
        vertical: Optional[VerticalAlignment]
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(
        self
    ) -> Union[Tuple[MaybeType, bool], Tuple[MaybeType, MaybeType]]: ...

class AlignComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    def __init__(
        self,
        children: List[VisualComponent],
        horizontal: Optional[ConstantValueProvider] = ...,
        vertical: Optional[ConstantValueProvider] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
