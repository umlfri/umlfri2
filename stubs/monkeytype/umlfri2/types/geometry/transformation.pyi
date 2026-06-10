from typing import Union
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.size import Size
from umlfri2.types.geometry.vector import Vector


class Transformation:
    def __init__(
        self,
        m11: Union[float, int],
        m12: Union[float, int],
        m21: Union[float, int],
        m22: Union[float, int],
        offset_x: Union[float, int],
        offset_y: Union[float, int]
    ) -> None: ...
    def __mul__(
        self,
        other: Transformation
    ) -> Transformation: ...
    @property
    def m11(self) -> Union[float, int]: ...
    @property
    def m12(self) -> Union[float, int]: ...
    @property
    def m21(self) -> Union[float, int]: ...
    @property
    def m22(self) -> Union[float, int]: ...
    @staticmethod
    def make_rotation(
        alpha: Union[float, int],
        center: Point = ...
    ) -> Transformation: ...
    @staticmethod
    def make_scale2(
        scale: Size,
        center: Point = ...
    ) -> Transformation: ...
    @staticmethod
    def make_translate(
        delta: Union[Vector, Point]
    ) -> Transformation: ...
    @property
    def offset_x(self) -> Union[float, int]: ...
    @property
    def offset_y(self) -> Union[float, int]: ...
