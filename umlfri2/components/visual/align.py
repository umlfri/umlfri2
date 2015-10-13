from .visualcomponent import VisualComponent, VisualObject


class AlignObject(VisualObject):
    def __init__(self, child, horizontal, vertical):
        self.__child = child
        self.__horizontal = horizontal
        self.__vertical = vertical
        self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        x, y, w, h = bounds
        
        w_inner, h_inner = self.__child_size
        
        if self.__horizontal == 'center':
            x += (w - w_inner) // 2
            w = w_inner
        elif self.__horizontal == 'left':
            w = w_inner
        elif self.__horizontal == 'right':
            x += w - w_inner
            w = w_inner
        
        if self.__vertical == 'center':
            y += (h - h_inner) // 2
            h = h_inner
        elif self.__vertical == 'top':
            h = h_inner
        elif self.__vertical == 'bottom':
            y += h - h_inner
            h = h_inner
        
        self.__child.assign_bounds((x, y, w, h))
    
    def get_minimal_size(self):
        return self.__child_size
    
    def draw(self, canvas, shadow, shadow_shift):
        self.__child.draw(canvas, shadow, shadow_shift)


class Align(VisualComponent):
    def __init__(self, children, horizontal: id=None, vertical: id=None):
        super().__init__(children)
        self.__horizontal = horizontal
        self.__vertical = vertical
    
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            return AlignObject(
                child._create_object(local, ruler),
                self.__horizontal,
                self.__vertical
            )
