from _weakref import ref
from weakref import WeakSet

from ..cache import ModelTemporaryDataCache
from umlfri2.types.geometry import Point, Rectangle, Size


class ElementVisual:
    def __init__(self, diagram, object):
        self.__cache = ModelTemporaryDataCache(self.__create_appearance_object)
        self.__cache.depend_on(object.cache)
        
        self.__cache.depend_on(self.__cache)
        
        self.__diagram = ref(diagram)
        
        self.__object = object
        self.__cached_appearance = None
        self.__position = Point(0, 0)
        self.__size = None
        self.__connections = WeakSet()
    
    def add_connection(self, connection):
        if connection.source != self and connection.destination != self:
            raise Exception("Cannot add connection not connected to the element")
        
        self.__connections.add(connection)
    
    def remove_connection(self, connection):
        if connection.source != self and connection.destination != self:
            raise Exception("Cannot remove connection not connected to the element")
        
        self.__connections.remove(connection)
    
    @property
    def cache(self):
        return self.__cache
    
    @property
    def object(self):
        return self.__object
    
    @property
    def diagram(self):
        return self.__diagram()
    
    @property
    def connections(self):
        yield from self.__connections
    
    def get_position(self, ruler):
        self.__cache.ensure_valid(ruler=ruler)
        
        return self.__position
    
    def get_size(self, ruler):
        self.__cache.ensure_valid(ruler=ruler)
        
        return self.__size
    
    def get_minimal_size(self, ruler):
        self.__cache.ensure_valid(ruler=ruler)
        
        return self.__cached_appearance.get_minimal_size()
    
    def get_bounds(self, ruler):
        self.__cache.ensure_valid(ruler=ruler)
        
        return Rectangle.from_point_size(self.__position, self.__size)
    
    def draw(self, canvas):
        self.__cache.ensure_valid(ruler=canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)

    def resize(self, ruler, new_size):
        self.__size = new_size
        
        self.__cache.invalidate()
    
    def move(self, ruler, new_position):
        self.__position = new_position
        
        self.__cache.invalidate()
    
    def is_at_position(self, ruler, position):
        return self.get_bounds(ruler).contains(position)
    
    def is_resizable(self, ruler):
        self.__cache.ensure_valid(ruler=ruler)
        
        return self.__cached_appearance.is_resizable()

    def __create_appearance_object(self, ruler):
        self.__cached_appearance = self.__object.create_appearance_object(ruler)
        self.__cached_appearance.move(self.__position)
        min_size = self.__cached_appearance.get_minimal_size()
        if self.__size is None or (self.__size.width < min_size.width and self.__size.height < min_size.height):
            self.__size = min_size
        else:
            resizable_x, resizable_y = self.__cached_appearance.is_resizable()
            if self.__size.width < min_size.width or not resizable_x:
                self.__size = Size(min_size.width, self.__size.height)
            elif self.__size.height < min_size.height or not resizable_y:
                self.__size = Size(self.__size.width, min_size.height)
            
            self.__cached_appearance.resize(self.__size)
