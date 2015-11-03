import math


class Vector:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
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
    
    def __neg__(self):
        return Vector(-self.__x, -self.__y)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.__x * other, self.__y * other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.__x / other, self.__y / other)
