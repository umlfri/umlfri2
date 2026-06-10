from umlfri2.application.drawingarea.drawingareacursor import DrawingAreaCursor
from umlfri2.application.drawingarea.selectionpointposition import SelectionPointPosition
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.rectangle import Rectangle


class ResizeElementAction:
    def __init__(
        self,
        element: ElementVisual,
        horizontal: SelectionPointPosition,
        vertical: SelectionPointPosition
    ) -> None: ...
    @property
    def box(self) -> Rectangle: ...
    @property
    def cursor(self) -> DrawingAreaCursor: ...
    def mouse_down(self, point: Point) -> None: ...
    def mouse_move(self, point: Point) -> None: ...
    def mouse_up(self) -> None: ...
