from __future__ import annotations

from typing import Union

from .vector import Vector


class Size:
    def __init__(self, width: float, height: float) -> None:
        self.__width = width
        self.__height = height
    
    @property
    def width(self) -> float:
        return self.__width
    
    @property
    def height(self) -> float:
        return self.__height
    
    def as_vector(self) -> Vector:
        return Vector(self.__width, self.__height)
    
    def rotate(self) -> Vector:
        return Vector(self.__height, self.__width)
    
    def __mul__(self, other: Union[int, float]) -> Size:
        return Size(self.__width * other, self.__height * other)
    
    def __str__(self) -> str:
        return "{0},{1}".format(self.__width, self.__height)
    
    def __repr__(self) -> str:
        return "<Size {0}>".format(self)
