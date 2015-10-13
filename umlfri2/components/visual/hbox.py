from .visualcomponent import VisualComponent, VisualObject


class HBoxObject(VisualObject):
    def __init__(self, children):
        self.__children = children
        
        self.__children_sizes = [child.get_minimal_size() for child in children]
    
    def assign_bounds(self, bounds):
        x, y, w, h = bounds
        
        if self.__children:
            for size, child in zip(self.__children_sizes, self.__children):
                child.assign_bounds((x, y, size[0], h))
                x += size[0]
    
    def get_minimal_size(self):
        w_all, h_all = zip(self.__children_sizes)
        return sum(w_all), max(h_all)
    
    def draw(self, canvas, shadow, shadow_shift):
        for child in self.__children:
            child.draw(canvas, shadow, shadow_shift)

class HBox(VisualComponent):
    def _create_object(self, context, ruler):
        children = [child._create_object(local, ruler) for local, child in self._get_children(context)]
        
        return HBoxObject(children)
