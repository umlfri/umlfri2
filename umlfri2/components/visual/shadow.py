from umlfri2.components.expressions import ConstantExpression
from umlfri2.types.color import Color
from .visualcomponent import VisualComponent


class Shadow(VisualComponent):
    def __init__(self, children, color: Color=None, padding: int=None):
        super().__init__(children)
        self.__color = color or ConstantExpression(Color.get_color("lightgray"))
        self.__padding = padding or ConstantExpression(5)
    
    def get_size(self, context, ruler):
        for local, child in self._get_children(context):
            w, h = child.get_size(local, ruler)
            padding = self.__padding(context)
            return w + padding, h + padding
    
    def draw(self, context, canvas, bounds, shadow=None):
        (x, y, w, h), (w_inner, h_inner) = self._compute_bounds(context, canvas.get_ruler(), bounds)
        
        color = shadow or self.__color(context)
        padding = self.__padding(context)
        
        for local, child in self._get_children(context):
            child.draw(local, canvas, (x + padding, y + padding, w, h), color)
            
            child.draw(local, canvas, (x, y, w, h), None)
            
            return
