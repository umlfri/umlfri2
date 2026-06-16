from ..base.componenttype import ComponentType as ComponentType
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from umlfri2.types.geometry import Size as Size
from umlfri2.ufl.types.basic import UflDecimalType as UflDecimalType
from typing import (
    List,
    Tuple,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.ufl.components.graphic.path import (
    PathComponent,
    PathObject,
)
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class GraphicsObject(VisualObject):
    def __init__(self, children: List[PathObject]) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...

class GraphicsComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    CHILDREN_TYPE: Incomplete
    def __init__(
        self,
        children: List[PathComponent],
        width: ConstantValueProvider,
        height: ConstantValueProvider
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
