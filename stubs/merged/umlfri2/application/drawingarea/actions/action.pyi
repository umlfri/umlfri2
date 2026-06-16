from ..drawingareacursor import DrawingAreaCursor as DrawingAreaCursor
from _typeshed import Incomplete
from typing import NamedTuple
from typing import (
    Callable,
    Tuple,
    Union,
)
from umlfri2.application.application import Application
from umlfri2.application.drawingarea.actions.addelement import AddElementAction
from umlfri2.application.drawingarea.actions.addtypedconnection import AddTypedConnectionAction
from umlfri2.application.drawingarea.drawingarea import DrawingArea
from umlfri2.application.drawingarea.drawingareacursor import DrawingAreaCursor
from umlfri2.application.drawingarea.snapping.snapping import Snapping
from umlfri2.types.geometry.point import Point


class ActionMenuItem(NamedTuple):
    icon: Incomplete
    text: Incomplete
    action: Incomplete

class Action:
    def __init__(self) -> None: ...
    def associate(
        self,
        application: Application,
        drawing_area: DrawingArea
    ) -> None: ...
    def snap_to(self, snapping: Snapping) -> None: ...
    def after_finish(
        self,
        callback: Callable
    ) -> Union[AddTypedConnectionAction, AddElementAction]: ...
    @property
    def application(self) -> Application: ...
    @property
    def drawing_area(self) -> DrawingArea: ...
    @property
    def box(self) -> None: ...
    @property
    def path(self) -> None: ...
    @property
    def vertical_snapping_indicators(self) -> Tuple[()]: ...
    @property
    def horizontal_snapping_indicators(self) -> Tuple[()]: ...
    @property
    def finished(self) -> bool: ...
    @property
    def cursor(self) -> DrawingAreaCursor: ...
    @property
    def menu_to_show(self) -> None: ...
    def mouse_down(self, point) -> None: ...
    def mouse_move(self, point: Point) -> None: ...
    def mouse_up(self) -> None: ...
