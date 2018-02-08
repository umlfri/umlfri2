from umlfri2.types.geometry import Rectangle, Point
from umlfri2.types.threestate import Maybe

from ..base.component import Component
from .empty import EmptyObject


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
        res_x, res_y = self.__object.is_resizable()
        
        if res_x is Maybe:
            res_x = False
        if res_y is Maybe:
            res_y = False
        
        return res_x, res_y
    
    def draw(self, canvas):
        self.__object.draw(canvas, None)


class VisualContainerComponent(Component):
    def __init__(self, children):
        super().__init__(children)
    
    def create_visual_object(self, context, ruler):
        for local, child in self._get_children(context):
            return VisualObjectContainer(child._create_object(local, ruler))
        
        return VisualObjectContainer(EmptyObject())
    
    def compile(self, type_context):
        self._compile_children(type_context)
