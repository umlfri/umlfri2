import math


class Vector:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    @staticmethod
    def from_angle_length(angle, length):
        return Vector(math.cos(angle) * length, math.sin(angle) * length)
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @property
    def angle(self):
        return math.atan2(self.__y, self.__x)
    
    @property
    def length(self):
        return math.sqrt(self.__x**2 + self.__y**2)
    
    def __bool__(self):
        return self.__x != 0 and self.__y != 0
    
    def __neg__(self):
        return Vector(-self.__x, -self.__y)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.__x * other, self.__y * other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.__x / other, self.__y / other)
    
    def __str__(self):
        return "{0},{1}".format(self.__x, self.__y)
    
    def __repr__(self):
        return "<Vector {0}>".format(self)
