class VisualObjectContainer:
    def __init__(self, object):
        self.__object = object
        self.__position = (0, 0)
        self.__size = self.__object.get_minimal_size()
        
    def resize(self, new_size):
        if new_size is None:
            self.__size = self.__object.get_minimal_size()
        else:
            self.__size = new_size
    
    def move(self, new_position):
        self.__position = new_position
    
    def get_minimal_size(self):
        return self.__object.get_minimal_size()
    
    def draw(self, canvas):
        self.__object.assign_bounds(self.__position + self.__size)
        self.__object.draw(canvas, None)
