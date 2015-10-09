from ..expressions import ConstantExpression
from .visualcomponent import VisualComponent


class Padding(VisualComponent):
    def __init__(self, children, padding: int=None, left: int=None, right: int=None, top: int=None, bottom: int=None):
        super().__init__(children)
        
        if padding is not None:
            self.left = padding
            self.right = padding
            self.top = padding
            self.bottom = padding
        else:
            self.left = left or ConstantExpression(0)
            self.right = right or ConstantExpression(0)
            self.top = top or ConstantExpression(0)
            self.bottom = bottom or ConstantExpression(0)

    def get_size(self, context, ruler):
        for local, child in self._get_children(context):
            w, h = child.get_size(local, ruler)
            
            return (
                w + self.left(context) + self.right(context),
                h + self.top(context) + self.bottom(context)
            )
    
    def draw(self, context, canvas, bounds, shadow=None):
        (x, y, w, h), (w_inner, h_inner) = self._compute_bounds(context, canvas.get_ruler(), bounds)
        
        left = self.left(context)
        right = self.right(context)
        top = self.top(context)
        bottom = self.bottom(context)
        
        for local, child in self._get_children(context):
            child.draw(local, canvas, (x + left, y + top, w - left - right, h - top - bottom), shadow)
            
            return
