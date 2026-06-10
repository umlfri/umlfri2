from typing import (
    List,
    Optional,
    Tuple,
    Union,
)
from umlfri2.qtgui.rendering.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.color import Color
from umlfri2.types.geometry.path import Path
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.rectangle import Rectangle
from umlfri2.types.geometry.size import Size
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.components.visual.padding import (
    PaddingComponent,
    PaddingObject,
)
from umlfri2.ufl.components.visual.shadow import ShadowInfo
from umlfri2.ufl.components.visual.sizer import (
    SizerComponent,
    SizerObject,
)
from umlfri2.ufl.components.visual.textbox import (
    TextBoxComponent,
    TextBoxObject,
)
from umlfri2.ufl.components.visual.vbox import (
    VBoxComponent,
    VBoxObject,
)
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class CornerDefinition:
    def __init__(
        self,
        id: str,
        path: Path,
        ornament: Optional[Path],
        center: Point,
        corner: str
    ) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def ornament(self) -> Optional[Path]: ...
    @property
    def path(self) -> Path: ...


class RectangleComponent:
    def __init__(
        self,
        children: List[Union[SizerComponent, VBoxComponent, PaddingComponent, TextBoxComponent]],
        fill: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...,
        border: Optional[Union[DynamicValueProvider, ConstantValueProvider]] = ...,
        topleft: Optional[ConstantValueProvider] = ...,
        topright: Optional[ConstantValueProvider] = ...,
        bottomleft: Optional[ConstantValueProvider] = ...,
        bottomright: Optional[ConstantValueProvider] = ...,
        left: Optional[ConstantValueProvider] = ...,
        right: Optional[ConstantValueProvider] = ...,
        top: None = ...,
        bottom: None = ...
    ) -> None: ...
    def _create_object(
        self,
        context: Context,
        ruler: QTRuler
    ) -> Union[RoundedRectangleObject, RectangleObject]: ...
    def compile(self, type_context: TypeContext) -> None: ...


class RectangleObject:
    def __init__(
        self,
        child: Union[VBoxObject, TextBoxObject],
        fill: Color,
        border: Optional[Color]
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(
        self,
        canvas: QTPainterCanvas,
        shadow: Optional[ShadowInfo]
    ) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...


class RoundedRectangleObject:
    def __init__(
        self,
        child: Union[PaddingObject, SizerObject],
        fill: Color,
        border: Color,
        corners: Union[List[CornerDefinition], Tuple[None, None, None, None], List[Optional[CornerDefinition]]],
        sides: Union[List[Optional[SideDefinition]], Tuple[None, None, None, None]]
    ) -> None: ...
    def assign_bounds(self, bounds: Rectangle) -> None: ...
    def draw(
        self,
        canvas: QTPainterCanvas,
        shadow: Optional[ShadowInfo]
    ) -> None: ...
    def get_minimal_size(self) -> Size: ...
    def is_resizable(self) -> Tuple[bool, bool]: ...


class SideDefinition:
    def __init__(
        self,
        id: str,
        path: Path,
        ornament: None,
        center: Point,
        size: Size,
        side: str
    ) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def ornament(self) -> None: ...
    @property
    def path(self) -> Path: ...
    @property
    def size(self) -> Size: ...
