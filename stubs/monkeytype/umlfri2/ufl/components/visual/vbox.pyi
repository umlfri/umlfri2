from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Tuple,
    Union,
)
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.size import Size
from umlfri2.types.threestate import MaybeType
from umlfri2.ufl.components.base.component import Component
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.visual.rectangle import RectangleComponent
from umlfri2.ufl.components.visual.sizer import SizerComponent


class VBoxComponent:
    def __init__(
        self,
        children: List[Component],
        expand: Union[Dict[RectangleComponent, ConstantValueProvider], Dict[SizerComponent, ConstantValueProvider]]
    ) -> None: ...


class VBoxObject:
    def _combine_resizable(
        self,
        ret_x: Union[MaybeType, bool],
        ret_y: MaybeType,
        child_x: Union[MaybeType, bool],
        child_y: Union[MaybeType, bool],
        expand: bool
    ) -> Union[Tuple[bool, MaybeType], Tuple[MaybeType, MaybeType]]: ...
    def _compute_size(self, all_widths: Iterator[Any], all_heights: Iterator[Any]) -> Size: ...
    def _get_size_component(self, size: Size) -> int: ...
    def _new_position(
        self,
        position: Point,
        size: Size
    ) -> Point: ...
    def _new_size(
        self,
        size: Size,
        whole_size: Size,
        delta: int
    ) -> Size: ...
