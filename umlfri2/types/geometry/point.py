from __future__ import annotations

from typing import TYPE_CHECKING, Union

from .size import Size
from .vector import Vector

if TYPE_CHECKING:
    from .transformation import Transformation


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y
    
    @property
    def x(self) -> float:
        return self.__x
    
    @property
    def y(self) -> float:
        return self.__y
    
    def as_vector(self) -> Vector:
        return Vector(self.__x, self.__y)
    
    def as_size(self) -> Size:
        return Size(self.__x, self.__y)
    
    def round(self) -> Point:
        return Point(int(round(self.__x)), int(round(self.__y)))
    
    def __sub__(self, other: object) -> Union[Vector, Point]:
        if isinstance(other, Point):
            return Vector(self.__x - other.__x, self.__y - other.__y)
        elif isinstance(other, Vector):
            return Point(self.__x - other.x, self.__y - other.y)
        else:
            return NotImplemented
    
    def __add__(self, other: object) -> Point:
        if isinstance(other, Vector):
            return Point(self.__x + other.x, self.__y + other.y)
        else:
            return NotImplemented
    
    def transform(self, matrix: Transformation) -> Point:
        return Point(
            matrix.m11*self.__x + matrix.m21*self.__y + matrix.offset_x,
            matrix.m12*self.__x + matrix.m22*self.__y + matrix.offset_y
        )
    
    def __str__(self) -> str:
        return "{0},{1}".format(self.__x, self.__y)
    
    def __repr__(self) -> str:
        return "<Point {0}>".format(self)
    
    def __hash__(self) -> int:
        return hash(self.__x) + hash(self.__y) << 4
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.__x == other.__x and self.__y == other.__y

    @staticmethod
    def parse(param: str) -> Point:
        x, y = param.split(",")
        return Point(float(x), float(y))
