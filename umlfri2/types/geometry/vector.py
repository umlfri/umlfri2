from __future__ import annotations

import math
from typing import Union


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y
    
    @staticmethod
    def from_angle_length(angle: float, length: float) -> Vector:
        return Vector(math.cos(angle) * length, math.sin(angle) * length)
    
    @property
    def x(self) -> float:
        return self.__x
    
    @property
    def y(self) -> float:
        return self.__y
    
    @property
    def angle(self) -> float:
        return math.atan2(self.__y, self.__x)
    
    @property
    def length(self) -> float:
        return math.sqrt(self.__x**2 + self.__y**2)
    
    def __bool__(self) -> bool:
        return self.__x != 0 or self.__y != 0
    
    def __neg__(self) -> Vector:
        return Vector(-self.__x, -self.__y)
    
    def __mul__(self, other: Union[int, float]) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.__x * other, self.__y * other)
    
    def __truediv__(self, other: Union[int, float]) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.__x / other, self.__y / other)
    
    def __str__(self) -> str:
        return "{0},{1}".format(self.__x, self.__y)
    
    def __repr__(self) -> str:
        return "<Vector {0}>".format(self)
