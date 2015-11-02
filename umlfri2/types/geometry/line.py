from .point import Point


class Line:
    def __init__(self, p1, p2, p3=None, p4=None):
        if p3 is None and p4 is None:
            self.__x1 = p1.x
            self.__y1 = p1.y
            self.__x2 = p2.x
            self.__y2 = p2.y
        else:
            self.__x1 = p1
            self.__y1 = p2
            self.__x2 = p3
            self.__y2 = p4
    
    @property
    def first(self):
        return Point(self.__x1, self.__y1)
    
    @property
    def second(self):
        return Point(self.__x2, self.__y2)
    
    def intersect(self, other):
        if isinstance(other, Line):
            pass
        else:
            return other.intersect(self)
