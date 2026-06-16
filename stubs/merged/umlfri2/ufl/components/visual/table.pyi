from ..base.componenttype import ComponentType as ComponentType
from ..base.helpercomponent import HelperComponent as HelperComponent
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from umlfri2.types.geometry import Rectangle as Rectangle, Size as Size
from umlfri2.types.threestate import Maybe as Maybe
from typing import (
    Any,
    List,
    Tuple,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.types.threestate import MaybeType
from umlfri2.ufl.components.common.foreach import ForEachComponent
from umlfri2.ufl.components.visual.textbox import TextBoxObject
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class TableObject(VisualObject):
    def __init__(self, table: List[Union[List[TextBoxObject], Any]]) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def is_resizable(self) -> Tuple[MaybeType, MaybeType]: ...

class TableRow(HelperComponent):
    CHILDREN_TYPE: Incomplete
    def compile(self, type_context: TypeContext) -> None: ...

class TableColumn(HelperComponent):
    CHILDREN_TYPE: Incomplete
    def compile(self, type_context) -> None: ...

class TableComponent(VisualComponent):
    CHILDREN_TYPE: Incomplete
    def __init__(self, children: List[ForEachComponent]) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
