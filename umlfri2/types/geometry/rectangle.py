from .point import Point
from .size import Size


class Rectangle:
    def __init__(self, p1, p2, p3 = None, p4 = None):
        if p3 is None and p4 is None:
            self.__x = p1.x
            self.__y = p1.y
            self.__width = p2.width
            self.__height = p2.height
        else:
            self.__x = p1
            self.__y = p2
            self.__width = p3
            self.__height = p4
    
    @property
    def top_left(self):
        return Point(self.__x, self.__y)
    
    @property
    def top_right(self):
        return Point(self.__x + self.__width, self.__y)
    
    @property
    def bottom_left(self):
        return Point(self.__x, self.__y + self.__height)
    
    @property
    def bottom_right(self):
        return Point(self.__x + self.__width, self.__y + self.__height)
    
    @property
    def size(self):
        return Size(self.__width, self.__height)
    
    @property
    def x1(self):
        return self.__x
    
    @property
    def y1(self):
        return self.__y
    
    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
    
    @property
    def x2(self):
        return self.__x + self.__width
    
    @property
    def y2(self):
        return self.__y + self.__height
    
    def contains(self, point):
        if point.x < self.__point.x or point.y < self.__point.y:
            return False
        
        x2 = self.__point.x + self.__size.width
        y2 = self.__point.y + self.__size.height
        
        if point.x > x2 or point.y > y2:
            return False
        
        return True
