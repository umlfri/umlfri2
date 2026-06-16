from .actions import AddConnectionPointAction as AddConnectionPointAction, AddUntypedConnectionAction as AddUntypedConnectionAction, MoveConnectionLabelAction as MoveConnectionLabelAction, MoveConnectionPointAction as MoveConnectionPointAction, MoveSelectionAction as MoveSelectionAction, RemoveConnectionPointAction as RemoveConnectionPointAction, ResizeElementAction as ResizeElementAction
from .selectionpointposition import SelectionPointPosition as SelectionPointPosition
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionHiddenEvent as ConnectionHiddenEvent, ElementHiddenEvent as ElementHiddenEvent, SelectionChangedEvent as SelectionChangedEvent
from umlfri2.model.connection import ConnectionVisual as ConnectionVisual
from umlfri2.model.element import ElementVisual as ElementVisual
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import LineStyle as LineStyle
from umlfri2.types.geometry import Line as Line, PathBuilder as PathBuilder, Point as Point, Rectangle as Rectangle, Size as Size, Transformation as Transformation, Vector as Vector
from typing import (
    Any,
    Iterator,
    Optional,
    Union,
)
from umlfri2.application.application import Application
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.rectangle import Rectangle


class Selection:
    SELECTION_COLOR: Incomplete
    SELECTION_SIZE: int
    SELECTION_POINT_COLOR: Incomplete
    SELECTION_POINT_SIZE: int
    LABEL_LINE_MINIMAL_DISTANCE: int
    ICON_COLOR: Incomplete
    ICON_COLOR_BACKGROUND: Incomplete
    CONNECTION_ICON_SHIFT: Incomplete
    CONNECTION_ICON: Incomplete
    CONNECTION_ICON_BOUNDS: Incomplete
    def __init__(
        self,
        application: Application,
        diagram: Diagram
    ) -> None: ...
    @property
    def selected_visuals(self) -> Generator[Incomplete, Incomplete]: ...
    @property
    def selected_elements(self) -> Iterator[ElementVisual]: ...
    @property
    def selected_connection(self) -> ConnectionVisual: ...
    @property
    def selected_diagram(self) -> Diagram: ...
    @property
    def diagram(self) -> Diagram: ...
    def select(
        self,
        visual: Optional[Union[ElementVisual, ConnectionVisual]]
    ) -> None: ...
    def select_all(self) -> None: ...
    def deselect_all(self) -> None: ...
    def add_to_selection(
        self,
        visual: Union[ElementVisual, ConnectionVisual]
    ) -> None: ...
    def remove_from_selection(self, visual) -> None: ...
    def toggle_select(self, visual: ElementVisual) -> None: ...
    def select_at(self, point: Point) -> None: ...
    def select_in_area(self, area: Rectangle) -> None: ...
    def draw_for(
        self,
        canvas: QTPainterCanvas,
        visual: Union[ElementVisual, ConnectionVisual]
    ) -> None: ...
    def draw_selected(self, canvas, selection: bool = False, transparent: bool = False) -> None: ...
    def get_action_at(self, position: Point, shift_pressed: bool) -> Any: ...
    def is_selection_at(self, position: Point) -> bool: ...
    def is_selected(self, visual): ...
    def get_bounds(self, include_connections: bool = True) -> Rectangle: ...
    @property
    def is_diagram_selected(self) -> bool: ...
    @property
    def is_connection_selected(self) -> bool: ...
    @property
    def is_element_selected(self) -> bool: ...
    @property
    def size(self): ...
    def get_lonely_selected_visual(
        self
    ) -> Union[ElementVisual, ConnectionVisual]: ...
