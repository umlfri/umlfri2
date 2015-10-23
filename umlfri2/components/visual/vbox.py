from umlfri2.types.geometry import Size, Rectangle
from .visualcomponent import VisualComponent, VisualObject


class VBoxObject(VisualObject):
    def __init__(self, children):
        self.__children = children
        
        self.__children_sizes = [child.get_minimal_size() for child in children]
    
    def assign_bounds(self, bounds):
        x = bounds.x1
        y = bounds.y1
        w = bounds.width
        
        if self.__children:
            for size, child in zip(self.__children_sizes, self.__children):
                child.assign_bounds(Rectangle(x, y, w, size.height))
                y += size.height
    
    def get_minimal_size(self):
        return Size(max(s.width for s in self.__children_sizes),
                    sum(s.height for s in self.__children_sizes))
    
    def draw(self, canvas, shadow):
        for child in self.__children:
            child.draw(canvas, shadow)

class VBoxComponent(VisualComponent):
    def _create_object(self, context, ruler):
        children = [child._create_object(local, ruler) for local, child in self._get_children(context)]
        
        return VBoxObject(children)
    
    def compile(self, variables):
        self._compile_children(variables)
