from typing import (
    Dict,
    List,
    Tuple,
    Type,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.types.threestate import MaybeType
from umlfri2.ufl.components.base.component import Component
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.visual.empty import EmptyObject
from umlfri2.ufl.components.visual.hbox import HBoxObject
from umlfri2.ufl.components.visual.rectangle import RectangleComponent
from umlfri2.ufl.components.visual.sizer import SizerComponent
from umlfri2.ufl.components.visual.vbox import VBoxObject
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class BoxComponent:
    def __init__(
        self,
        object_type: Union[Type[HBoxObject], Type[VBoxObject]],
        children: List[Component],
        expand: Union[Dict[SizerComponent, ConstantValueProvider], Dict[RectangleComponent, ConstantValueProvider]]
    ) -> None: ...
    def _create_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> Union[VBoxObject, HBoxObject, EmptyObject]: ...
    def compile(self, type_context: TypeContext) -> None: ...


class BoxObject:
    def __init__(self, children: List[BoxChild]) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(
        self
    ) -> Union[Tuple[bool, MaybeType], Tuple[bool, bool], Tuple[MaybeType, MaybeType]]: ...
