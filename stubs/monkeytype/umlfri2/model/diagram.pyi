from typing import (
    Any,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
from umlfri2.application.drawingarea.selection import Selection
from umlfri2.metamodel.diagramtype import DiagramType
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.model.project import Project
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.ufl.dialog.dialog import UflDialog
from umlfri2.ufl.dialog.options import UflDialogOptions
from umlfri2.ufl.objects.immutable.object import UflObject
from umlfri2.ufl.objects.patch.object import UflObjectPatch
from uuid import UUID


class Diagram:
    def __init__(
        self,
        parent: ElementObject,
        type: DiagramType,
        save_id: Optional[UUID] = ...
    ) -> None: ...
    def apply_ufl_patch(self, patch: UflObjectPatch) -> None: ...
    def change_z_order_many(
        self,
        z_order_visuals: List[Tuple[int, ElementVisual]]
    ) -> None: ...
    @property
    def connections(self) -> Iterator[ConnectionVisual]: ...
    def contains(
        self,
        object: Union[ConnectionVisual, ConnectionObject, ElementVisual, ElementObject]
    ) -> bool: ...
    def create_ufl_dialog(
        self,
        options: UflDialogOptions = ...
    ) -> UflDialog: ...
    @property
    def data(self) -> UflObject: ...
    def draw(
        self,
        canvas: QTPainterCanvas,
        selection: Optional[Selection] = ...,
        transparent: bool = ...
    ) -> None: ...
    def draw_background(self, canvas: QTPainterCanvas) -> None: ...
    @property
    def elements(self) -> Iterator[ElementVisual]: ...
    def get_bounds(self, ruler: QTRuler) -> Rectangle: ...
    def get_display_name(self) -> str: ...
    def get_size(self, ruler: QTRuler) -> Size: ...
    def get_visual_above(
        self,
        ruler: QTRuler,
        visual: ElementVisual,
        skip: Set[Any] = ...
    ) -> None: ...
    def get_visual_at(
        self,
        ruler: QTRuler,
        position: Point
    ) -> Optional[Union[ConnectionVisual, ElementVisual]]: ...
    def get_visual_below(
        self,
        ruler: QTRuler,
        visual: ElementVisual,
        skip: Tuple[ElementVisual] = ...
    ) -> Optional[ElementVisual]: ...
    def get_z_order(
        self,
        visual: Union[ConnectionVisual, ElementVisual]
    ) -> int: ...
    @property
    def has_ufl_dialog(self) -> bool: ...
    @property
    def parent(self) -> ElementObject: ...
    @property
    def project(self) -> Project: ...
    def remove(
        self,
        visual: Union[ConnectionVisual, ElementVisual]
    ) -> None: ...
    @property
    def save_id(self) -> UUID: ...
    def show(
        self,
        object: Union[ConnectionObject, ElementObject]
    ) -> Union[ConnectionVisual, ElementVisual]: ...
    @property
    def type(self) -> DiagramType: ...


class DiagramValueGenerator:
    def __init__(
        self,
        parent: ElementObject,
        type: DiagramType
    ) -> None: ...
    def for_name(self, name: str) -> DiagramValueGenerator: ...
    def get_parent_name(self) -> str: ...
    def has_value(self, value: str) -> bool: ...
