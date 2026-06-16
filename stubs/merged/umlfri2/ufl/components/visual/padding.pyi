from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from umlfri2.types.geometry import Rectangle as Rectangle, Size as Size
from umlfri2.ufl.types.basic import UflIntegerType as UflIntegerType
from typing import (
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
from umlfri2.ufl.components.visual.align import AlignObject
from umlfri2.ufl.components.visual.ellipse import EllipseObject
from umlfri2.ufl.components.visual.table import TableObject
from umlfri2.ufl.components.visual.textbox import TextBoxObject
from umlfri2.ufl.components.visual.vbox import VBoxObject
from umlfri2.ufl.components.visual.visualcomponent import VisualComponent
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class PaddingObject(VisualObject):
    def __init__(
        self,
        child: Union[AlignObject, EllipseObject, TextBoxObject, VBoxObject, TableObject],
        left: int,
        right: int,
        top: int,
        bottom: int
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(
        self
    ) -> Union[Tuple[MaybeType, MaybeType], Tuple[bool, bool]]: ...

class PaddingComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    def __init__(
        self,
        children: List[VisualComponent],
        padding: Optional[ConstantValueProvider] = ...,
        left: Optional[ConstantValueProvider] = ...,
        right: Optional[ConstantValueProvider] = ...,
        top: Optional[ConstantValueProvider] = ...,
        bottom: Optional[ConstantValueProvider] = ...
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
