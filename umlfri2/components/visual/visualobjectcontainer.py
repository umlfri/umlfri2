from umlfri2.types.geometry import Rectangle, Point


class VisualObjectContainer:
    def __init__(self, object):
        self.__object = object
        self.__position = Point(0, 0)
        self.__size = self.__object.get_minimal_size()
    
    @property
    def size(self):
        return self.__size
    
    @property
    def position(self):
        return self.__position
    
    def resize(self, new_size):
        if new_size is None:
            self.__size = self.__object.get_minimal_size()
        else:
            self.__size = new_size
        self.__object.assign_bounds(Rectangle.from_point_size(self.__position, self.__size))
    
    def move(self, new_position):
        self.__position = new_position
        self.__object.assign_bounds(Rectangle.from_point_size(self.__position, self.__size))
    
    def get_minimal_size(self):
        return self.__object.get_minimal_size()
    
    def is_resizable(self):
        return self.__object.is_resizable()
    
    def draw(self, canvas):
        self.__object.draw(canvas, None)
