from __future__ import annotations

import math
from .point import Point


class Transformation:
    def __init__(self, m11: float, m12: float, m21: float, m22: float, offset_x: float, offset_y: float) -> None:
        self.__m11 = m11
        self.__m12 = m12
        self.__m21 = m21
        self.__m22 = m22
        self.__offset_x = offset_x
        self.__offset_y = offset_y
    
    @property
    def m11(self) -> float:
        return self.__m11
    
    @property
    def m12(self) -> float:
        return self.__m12
    
    @property
    def m21(self) -> float:
        return self.__m21
    
    @property
    def m22(self) -> float:
        return self.__m22
    
    @property
    def offset_x(self) -> float:
        return self.__offset_x
    
    @property
    def offset_y(self) -> float:
        return self.__offset_y
    
    def __mul__(self, other: object) -> Transformation:
        if isinstance(other, Transformation):
            return Transformation(
                self.__m11*other.__m11 + self.__m21*other.__m12,
                self.__m12*other.__m11 + self.__m22*other.__m12,
                self.__m11*other.__m21 + self.__m21*other.__m22,
                self.__m12*other.__m21 + self.__m22*other.__m22,
                self.__m11*other.__offset_x + self.__m21*other.__offset_y + self.__offset_x,
                self.__m12*other.__offset_x + self.__m22*other.__offset_y + self.__offset_y
            )
        else:
            return NotImplemented
    
    @staticmethod
    def make_rotation(alpha: float, center: Point = Point(0, 0)) -> Transformation:
        sin = math.sin(alpha)
        cos = math.cos(alpha)
        
        return Transformation(
            cos, sin,
            -sin, cos,
            center.x + sin*center.y - cos*center.x,
            center.y - sin*center.x - cos*center.y
        )
    
    @staticmethod
    def make_scale(scale: float, center: Point = Point(0, 0)) -> Transformation:
        return Transformation(
            scale, 0,
            0, scale,
            center.x - scale*center.x,
            center.y - scale*center.y
        )
    
    @staticmethod
    def make_scale2(scale: Size, center: Point = Point(0, 0)) -> Transformation:
        return Transformation(
            scale.width, 0,
            0, scale.height,
            center.x - scale.width*center.x,
            center.y - scale.height*center.y
        )
    
    @staticmethod
    def make_translate(delta: Vector) -> Transformation:
        return Transformation(
            1, 0,
            0, 1,
            delta.x, delta.y
        )
    
    @staticmethod
    def make_skew_x(alpha: float) -> Transformation:
        return Transformation(
            1, 0,
            math.tan(alpha), 1,
            0, 0
        )
    
    @staticmethod
    def make_skew_y(alpha: float) -> Transformation:
        return Transformation(
            1, math.tan(alpha),
            0, 1,
            0, 0
        )
    
    @staticmethod
    def make_identity() -> Transformation:
        return Transformation(
            1, 0,
            0, 1,
            0, 0
        )
