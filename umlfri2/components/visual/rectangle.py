from umlfri2.types.color import Color
from .visualcomponent import VisualComponent


class Rectangle(VisualComponent):
    def __init__(self, children, fill: Color=None, border: Color=None):
        super().__init__(children)
        self.__fill = fill
        self.__border = border
    
    def get_size(self, context, ruler):
        for local, child in self._get_children(context):
            return child.get_size(local, ruler)
    
    def draw(self, context, canvas, bounds, shadow=None):
        new_bounds, inner_size = self._compute_bounds(context, canvas.get_ruler(), bounds)
        
        if shadow:
            fill = shadow
            border = None
        else:
            fill = self.__fill(context)
            border = self.__border(context)
        
        canvas.draw_rectangle(new_bounds[:2], new_bounds[2:], border, fill)
        
        if not shadow:
            for local, child in self._get_children(context):
                child.draw(local, canvas, new_bounds, None)
                
                return
