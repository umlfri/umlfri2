from .empty import EmptyObject as EmptyObject
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from typing import NamedTuple
from umlfri2.types.geometry import Rectangle as Rectangle, Size as Size
from umlfri2.types.threestate import Maybe as Maybe
from umlfri2.ufl.types.basic import UflBoolType as UflBoolType
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

class BoxChild(NamedTuple):
    child: Incomplete
    expand: Incomplete

class BoxObject(VisualObject):
    def __init__(self, children: List[BoxChild]) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(
        self
    ) -> Union[Tuple[bool, MaybeType], Tuple[bool, bool], Tuple[MaybeType, MaybeType]]: ...

class BoxComponent(VisualComponent):
    CHILDREN_ATTRIBUTES: Incomplete
    def __init__(
        self,
        object_type: Union[Type[HBoxObject], Type[VBoxObject]],
        children: List[Component],
        expand: Union[Dict[SizerComponent, ConstantValueProvider], Dict[RectangleComponent, ConstantValueProvider]]
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
