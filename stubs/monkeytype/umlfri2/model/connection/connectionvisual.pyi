from typing import (
    Iterator,
    Optional,
)
from umlfri2.model.cache import ModelTemporaryDataCache
from umlfri2.model.connection.connectionlabel import ConnectionLabel
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.rectangle import Rectangle


class ConnectionVisual:
    def __init__(
        self,
        diagram: Diagram,
        object: ConnectionObject,
        source: ElementVisual,
        destination: ElementVisual
    ) -> None: ...
    def _reverse(self) -> None: ...
    def add_point(
        self,
        ruler: QTRuler,
        index: Optional[int],
        point: Point
    ) -> None: ...
    @property
    def cache(self) -> ModelTemporaryDataCache: ...
    @property
    def destination(self) -> ElementVisual: ...
    @property
    def diagram(self) -> Diagram: ...
    def draw(self, canvas: QTPainterCanvas) -> None: ...
    def get_bounds(self, ruler: QTRuler) -> Rectangle: ...
    def get_label(self, id: str) -> ConnectionLabel: ...
    def get_labels(self) -> Iterator[ConnectionLabel]: ...
    def get_point(self, ruler: QTRuler, id: int) -> Point: ...
    def get_points(
        self,
        ruler: QTRuler,
        source_and_end: bool = ...,
        element_centers: bool = ...
    ) -> Iterator[Point]: ...
    def is_at_position(
        self,
        ruler: QTRuler,
        position: Point
    ) -> bool: ...
    @property
    def is_identity(self) -> bool: ...
    def move_point(
        self,
        ruler: QTRuler,
        index: int,
        point: Point
    ) -> None: ...
    @property
    def object(self) -> ConnectionObject: ...
    def remove_point(self, ruler: QTRuler, index: int) -> None: ...
    @property
    def source(self) -> ElementVisual: ...
