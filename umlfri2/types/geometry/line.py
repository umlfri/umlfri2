from .point import Point


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
    
    @staticmethod
    def from_point_point(p1, p2):
        return Line(p1.x, p1.y, p2.x, p2.y)
    
    @property
    def first(self):
        return Point(self.__x1, self.__y1)
    
    @property
    def second(self):
        return Point(self.__x2, self.__y2)
    
    def get_abc(self):
        # computed by wolframalpha
        # http://www.wolframalpha.com/input/?i=solve+x1%2Bb*y1%2Bc%3D0%2Cx2%2Bb*y2%2Bc%3D0+for+a%2Cb%2Cc
        if self.__y1 == self.__y2:
            return 0, 1, -self.__y1
        else:
            return 1, \
                   (self.__x2 - self.__x1) / (self.__y1 - self.__y2), \
                   (self.__x1*self.__y2 - self.__x2*self.__y1) / (self.__y1 - self.__y2)
    
    def intersect(self, other):
        if isinstance(other, Line):
            a1, b1, c1 = self.get_abc()
            a2, b2, c2 = other.get_abc()
            
            # computed by wolframalpha
            # http://www.wolframalpha.com/input/?i=solve+a1*x%2Bb1*y%2Bc1%3D0%2Ca2*x%2Bb2*y%2Bc2%3D0+for+x%2Cy
            if a2*b1 == a1*b2:
                return
            
            x = int(round((b2*c1 - b1*c2)/(a2*b1 - a1*b2)))
            y = int(round((a2*c1 - a1*c2)/(a1*b2 - a2*b1)))
            
            if min(self.__x1, self.__x2) <= x <= max(self.__x1, self.__x2) and \
                    min(other.__x1, other.__x2) <= x <= max(other.__x1, other.__x2) and \
                    min(self.__y1, self.__y2) <= y <= max(self.__y1, self.__y2) and \
                    min(other.__y1, other.__y2) <= y <= max(other.__y1, other.__y2):
                yield Point(x, y)
        else:
            yield from other.intersect(self)
    
    def get_nearest_point_to(self, other):
        if isinstance(other, Point):
            a, b, c = self.get_abc()
            x = other.x
            y = other.y
            
            t = a*a + b*b
            # closest point according to wikipedia
            # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
            closest_x = (b*(b*x - a*y) - a*c) / t
            closest_y = (a*(-b*x + a*y) - b*c) / t
            
            if self.__x2 > self.__x1 > closest_x:
                return self.first
            if self.__x1 > self.__x2 > closest_x:
                return self.second
            if self.__x2 < self.__x1 < closest_x:
                return self.first
            if self.__x1 < self.__x2 < closest_x:
                return self.second
            if self.__y2 > self.__y1 > closest_y:
                return self.first
            if self.__y1 > self.__y2 > closest_y:
                return self.second
            if self.__y2 < self.__y1 < closest_y:
                return self.first
            if self.__y1 < self.__y2 < closest_y:
                return self.second
            
            return Point(closest_x, closest_y)
        else:
            return other.get_distance_to(self)
    
    def get_distance_to(self, other):
        if isinstance(other, Point):
            return (other - self.get_nearest_point_to(other)).length
        else:
            return other.get_distance_to(self)
    
    def __str__(self):
        return "[{0}, {1}], [{2}, {3}]".format(self.__x1, self.__y1, self.__x2, self.__y2)
    
    def __repr__(self):
        return "<Line {0}>".format(self)
