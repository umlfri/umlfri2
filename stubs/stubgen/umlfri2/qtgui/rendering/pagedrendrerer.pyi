from .qtpaintercanvas import QTPainterCanvas as QTPainterCanvas
from .qtruler import QTRuler as QTRuler
from umlfri2.types.geometry import Vector as Vector

class PagedRenderer:
    def __init__(self, device) -> None: ...
    def render_diagram(self, diagram) -> None: ...
