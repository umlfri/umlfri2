from .visualcomponent import VisualComponent

class Align(VisualComponent):
    def __init__(self, children, horizontal: id=None, vertical: id=None):
        super().__init__(children)
        self.__horizontal = horizontal
        self.__vertical = vertical
    
    def get_size(self, context, ruler):
        for local, child in self._get_children(context):
            return child.get_size(local, ruler)
    
    def draw(self, context, canvas, bounds, shadow=None):
        for local, child in self._get_children(context):
            (x, y, w, h), (w_inner, h_inner) = child._compute_bounds(local, canvas.get_ruler(), bounds)
            
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
            
            child.draw(local, canvas, (x, y, w, h), shadow)
            
            return
