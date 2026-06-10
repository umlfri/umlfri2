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


class AlignComponent:
    def __init__(
        self,
        children: List[VisualComponent],
        horizontal: Optional[ConstantValueProvider] = ...,
        vertical: Optional[ConstantValueProvider] = ...
    ) -> None: ...
    def _create_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> AlignObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class AlignObject:
    def __init__(
        self,
        child: Union[LineObject, VBoxObject, SizerObject, TextBoxObject, RectangleObject],
        horizontal: Optional[HorizontalAlignment],
        vertical: Optional[VerticalAlignment]
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(
        self
    ) -> Union[Tuple[MaybeType, bool], Tuple[MaybeType, MaybeType]]: ...
