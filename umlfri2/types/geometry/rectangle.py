from .point import Point
from .size import Size
from .line import Line


class Rectangle:
    def __init__(self, x, y, width, height):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
    
    @staticmethod
    def from_point_size(point, size):
        return Rectangle(point.x, point.y, size.width, size.height)
    
    @staticmethod
    def from_point_point(p1, p2):
        return Rectangle(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y)
    
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
    def center(self):
        return Point(self.__x + self.__width // 2, self.__y + self.__height // 2)
    
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
        if point.x < self.__x or point.y < self.__y:
            return False
        
        if point.x > self.x2 or point.y > self.y2:
            return False
        
        return True
    
    def intersect(self, other):
        intersections = set()
        for line in Line.from_point_point(self.top_left, self.top_right),\
                    Line.from_point_point(self.top_right, self.bottom_right),\
                    Line.from_point_point(self.bottom_right, self.bottom_left),\
                    Line.from_point_point(self.bottom_left, self.top_left):
            intersections.update(line.intersect(other))
        
        yield from intersections
    
    def __str__(self):
        return "[{0}, {1}], [{2}, {3}]".format(self.__x, self.__y, self.__x + self.__width, self.__y + self.__height)
    
    def __repr__(self):
        return "<Rectangle {0}>".format(self)
