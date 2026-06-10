from PyQt5.QtGui import QPainter
from typing import Optional
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.color import Color
from umlfri2.types.enums.linestyle import LineStyle
from umlfri2.types.font import Font
from umlfri2.types.geometry.path import Path
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.vector import Vector


class QTPainterCanvas:
    def __init__(self, painter: QPainter) -> None: ...
    def clear(self, color: Optional[Color] = ...) -> None: ...
    def draw_ellipse(
        self,
        rectangle: Rectangle,
        fg: Optional[Color] = ...,
        bg: Optional[Color] = ...,
        line_width: None = ...,
        line_style: None = ...
    ) -> None: ...
    def draw_line(
        self,
        start: Point,
        end: Point,
        fg: Color,
        line_width: Optional[int] = ...,
        line_style: Optional[LineStyle] = ...
    ) -> None: ...
    def draw_path(
        self,
        path: Path,
        fg: Optional[Color] = ...,
        bg: Optional[Color] = ...,
        line_width: Optional[int] = ...,
        line_style: Optional[LineStyle] = ...
    ) -> None: ...
    def draw_rectangle(
        self,
        rectangle: Rectangle,
        fg: Optional[Color] = ...,
        bg: Optional[Color] = ...,
        line_width: Optional[int] = ...,
        line_style: None = ...
    ) -> None: ...
    def draw_text(
        self,
        pos: Point,
        text: str,
        font: Font,
        fg: Color
    ) -> None: ...
    def get_ruler(self) -> QTRuler: ...
    def translate(self, delta: Vector) -> None: ...
    def zoom(self, zoom: float) -> None: ...
