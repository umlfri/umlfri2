from .vector import Vector


class Size:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
    
    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
    
    def as_vector(self):
        return Vector(self.__width, self.__height)
    
    def __str__(self):
        return "{0},{1}".format(self.__width, self.__height)
    
    def __repr__(self):
        return "<Size {0}>".format(self)
