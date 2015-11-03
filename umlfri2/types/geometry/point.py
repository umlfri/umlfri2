from .vector import Vector


class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    def as_vector(self):
        return Vector(self.__x, self.__y)
    
    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(self.__x - other.__x, self.__y - other.__y)
        elif isinstance(other, Vector):
            return Point(self.__x - other.x, self.__y - other.y)
        else:
            return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Point(self.__x + other.x, self.__y + other.y)
        else:
            return NotImplemented
    
    def transform(self, matrix):
        return Point(
            matrix.m11*self.__x + matrix.m12*self.__y + matrix.offset_x,
            matrix.m21*self.__x + matrix.m22*self.__y + matrix.offset_y
        )
    
    def __str__(self):
        return "{0},{1}".format(self.__x, self.__y)
    
    def __repr__(self):
        return "<Point {0}>".format(self)

    @staticmethod
    def parse(param):
        x, y = param.split(",")
        return Point(float(x), float(y))
