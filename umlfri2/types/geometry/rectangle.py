from .vector import Vector
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
        for line in self.all_lines:
            intersections.update(line.intersect(other))
        
        yield from intersections
    
    def get_nearest_point_to(self, other):
        distance = float('inf')
        point = None
        
        for line in self.all_lines:
            new_point = line.get_nearest_point_to(other)
            new_distance = (new_point - other).length
            if new_distance < distance:
                distance = new_distance
                point = new_point
        
        return point
    
    def is_overlapping(self, other):
        if self.x1 <= other.x1 <= self.x2 or other.x1 <= self.x1 <= other.x2:
            if self.y1 <= other.y1 <= self.y2 or other.y1 <= self.y1 <= other.y2:
                return True
        return False

    @property
    def all_lines(self):
        yield Line.from_point_point(self.top_left, self.top_right)
        yield Line.from_point_point(self.top_right, self.bottom_right)
        yield Line.from_point_point(self.bottom_right, self.bottom_left)
        yield Line.from_point_point(self.bottom_left, self.top_left)
    
    def normalize(self):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        
        if x1 > x2:
            x1, x2 = x2, x1
        
        if y1 > y2:
            y1, y2 = y2, y1
        
        return Rectangle(x1, y1, x2 - x1, y2 - y1)
    
    @staticmethod
    def combine_bounds(rectangles):
        x1 = float('inf')
        x2 = -float('inf')
        y1 = float('inf')
        y2 = -float('inf')
        
        found = False
        
        for rectangle in rectangles:
            found = True
            if rectangle.x1 < x1:
                x1 = rectangle.x1
            if rectangle.y1 < y1:
                y1 = rectangle.y1
            if rectangle.x2 > x2:
                x2 = rectangle.x2
            if rectangle.y2 > y2:
                y2 = rectangle.y2
        
        if found:
            return Rectangle(x1, y1, x2 - x1, y2 - y1)
        else:
            return Rectangle(0, 0, 0, 0)
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Rectangle.from_point_size(self.top_left + other, self.size)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Rectangle.from_point_size(self.top_left - other, self.size)
        return NotImplemented
    
    def __str__(self):
        return "[{0}, {1}], [{2}, {3}]".format(self.__x, self.__y, self.__x + self.__width, self.__y + self.__height)
    
    def __repr__(self):
        return "<Rectangle {0}>".format(self)
