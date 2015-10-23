import math
from .point import Point


class Transformation:
    def __init__(self, m11, m12, m21, m22, offsetX, offsetY):
        self.__m11 = m11
        self.__m12 = m12
        self.__m21 = m21
        self.__m22 = m22
        self.__offset_x = offsetX
        self.__offset_y = offsetY
    
    @property
    def m11(self):
        return self.__m11
    
    @property
    def m12(self):
        return self.__m12
    
    @property
    def m21(self):
        return self.__m21
    
    @property
    def m22(self):
        return self.__m22
    
    @property
    def offset_x(self):
        return self.__offset_x
    
    @property
    def offset_y(self):
        return self.__offset_y
    
    def __mul__(self, other):
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
    def make_rotation(alpha, center=Point(0, 0)):
        sin = math.sin(alpha)
        cos = math.cos(alpha)
        
        return Transformation(
            cos, sin,
            -sin, cos,
            center.x + sin*center.y - cos*center.x,
            center.y - sin*center.x - cos*center.y
        )
    
    @staticmethod
    def make_scale(scale, center=Point(0, 0)):
        return Transformation(
            scale, 0,
            0, scale,
            center.x - scale*center.x,
            center.y - scale*center.y
        )
    
    @staticmethod
    def make_scale2(scale, center=Point(0, 0)):
        return Transformation(
            scale.x, 0,
            0, scale.y,
            center.x - scale.x*center.x,
            center.y - scale.y*center.y
        )
    
    @staticmethod
    def make_translate(delta):
        return Transformation(
            1, 0,
            0, 1,
            delta.x, delta.y
        )
    
    @staticmethod
    def make_skew_x(alpha):
        return Transformation(
            1, 0,
            math.tan(alpha), 1,
            0, 0
        )
    
    @staticmethod
    def make_skew_y(alpha):
        return Transformation(
            1, math.tan(alpha),
            0, 1,
            0, 0
        )
    
    @staticmethod
    def make_identity():
        return Transformation(
            1, 0,
            0, 1,
            0, 0
        )
