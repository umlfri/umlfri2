from .visualcomponent import VisualComponent, VisualObject


class VBoxObject(VisualObject):
    def __init__(self, children):
        self.__children = children
        
        self.__children_sizes = [child.get_minimal_size() for child in children]
    
    def assign_bounds(self, bounds):
        x, y, w, h = bounds
        
        if self.__children:
            for size, child in zip(self.__children_sizes, self.__children):
                child.assign_bounds((x, y, w, size[1]))
                y += size[1]
    
    def get_minimal_size(self):
        w_all, h_all = zip(*self.__children_sizes)
        return max(w_all), sum(h_all)
    
    def draw(self, canvas, shadow):
        for child in self.__children:
            child.draw(canvas, shadow)

class VBox(VisualComponent):
    def _create_object(self, context, ruler):
        children = [child._create_object(local, ruler) for local, child in self._get_children(context)]
        
        return VBoxObject(children)
