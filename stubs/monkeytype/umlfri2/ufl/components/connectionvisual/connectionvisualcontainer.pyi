from typing import (
    List,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.types.geometry.point import Point
from umlfri2.ufl.components.connectionvisual.arrow import ConnectionArrowObject
from umlfri2.ufl.components.connectionvisual.line import ConnectionLineObject
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class ConnectionVisualContainerComponent:
    def _create_object(
        self,
        context: Context
    ) -> ConnectionVisualContainerObject: ...
    def compile(self, type_context: TypeContext) -> None: ...


class ConnectionVisualContainerObject:
    def __init__(
        self,
        children: List[Union[ConnectionLineObject, ConnectionArrowObject]]
    ) -> None: ...
    def assign_points(self, points: List[Point]) -> None: ...
    def draw(self, canvas: QTPainterCanvas) -> None: ...
