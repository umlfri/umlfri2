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


class TableComponent:
    def __init__(self, children: List[ForEachComponent]) -> None: ...
    def _create_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> TableObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class TableObject:
    def __init__(self, table: List[Union[List[TextBoxObject], Any]]) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(self, canvas: QTPainterCanvas, shadow: None) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(self) -> Tuple[MaybeType, MaybeType]: ...


class TableRow:
    def compile(self, type_context: TypeContext) -> None: ...
