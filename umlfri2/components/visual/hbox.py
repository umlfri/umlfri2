from umlfri2.types.geometry import Size, Point, Rectangle
from .visualcomponent import VisualComponent, VisualObject


class HBoxObject(VisualObject):
    def __init__(self, children):
        self.__children = children
        
        self.__children_sizes = [child.get_minimal_size() for child in children]
    
    def assign_bounds(self, bounds):
        x = bounds.x1
        y = bounds.y1
        h = bounds.height
        
        if self.__children:
            for size, child in zip(self.__children_sizes, self.__children):
                child.assign_bounds(Rectangle(x, y, size.width, h))
                x += size.height
    
    def get_minimal_size(self):
        if self.__children_sizes:
            return Size(sum(s.width for s in self.__children_sizes),
                        max(s.height for s in self.__children_sizes))
        else:
            return Size(0, 0)
    
    def draw(self, canvas, shadow):
        for child in self.__children:
            child.draw(canvas, shadow)

class HBoxComponent(VisualComponent):
    def _create_object(self, context, ruler):
        children = [child._create_object(local, ruler) for local, child in self._get_children(context)]
        
        return HBoxObject(children)
    
    def compile(self, variables):
        self._compile_children(variables)
