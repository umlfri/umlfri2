from ..base.component import Component as Component
from .empty import EmptyObject as EmptyObject
from umlfri2.types.geometry import Point as Point, Rectangle as Rectangle
from umlfri2.types.threestate import Maybe as Maybe
from typing import (
    List,
    Tuple,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.size import Size
from umlfri2.ufl.components.base.component import Component
from umlfri2.ufl.components.visual.empty import EmptyObject
from umlfri2.ufl.components.visual.rectangle import RectangleObject
from umlfri2.ufl.components.visual.shadow import ShadowObject
from umlfri2.ufl.components.visual.sizer import SizerObject
from umlfri2.ufl.components.visual.vbox import VBoxObject
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class VisualObjectContainer:
    def __init__(
        self,
        object: Union[ShadowObject, RectangleObject, EmptyObject, SizerObject, VBoxObject]
    ) -> None: ...
    @property
    def size(self) -> Size: ...
    @property
    def position(self) -> Point: ...
    def resize(self, new_size: Size) -> None: ...
    def move(self, new_position: Point) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...
    def draw(self, canvas: QTPainterCanvas) -> None: ...

class VisualContainerComponent(Component):
    def __init__(self, children: List[Component]) -> None: ...
    def create_visual_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> VisualObjectContainer: ...
    def compile(self, type_context: TypeContext) -> None: ...
