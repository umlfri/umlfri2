from ..expressions import ConstantExpression
from .visualcomponent import VisualComponent, VisualObject


class PaddingObject(VisualObject):
    def __init__(self, child, left, right, top, bottom):
        self.__child = child
        self.__left = left
        self.__right = right
        self.__top = top
        self.__bottom = bottom
        self.__child_size = self.__child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        x, y, w, h = bounds
        self.__child.assign_bounds((x + self.__left, y + self.__top,
            w - self.__left - self.__right, h - self.__top - self.__bottom))
    
    def get_minimal_size(self):
        w, h = self.__child_size
        return w + self.__left + self.__right, h + self.__top + self.__bottom
    
    def draw(self, canvas, shadow, shadow_shift):
        self.__child.draw(canvas, shadow, shadow_shift)


class Padding(VisualComponent):
    def __init__(self, children, padding: int=None, left: int=None, right: int=None, top: int=None, bottom: int=None):
        super().__init__(children)
        
        if padding is not None:
            self.__left = padding
            self.__right = padding
            self.__top = padding
            self.__bottom = padding
        else:
            self.__left = left or ConstantExpression(0)
            self.__right = right or ConstantExpression(0)
            self.__top = top or ConstantExpression(0)
            self.__bottom = bottom or ConstantExpression(0)
    
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            return PaddingObject(
                child._create_object(local, ruler),
                self.__left(local),
                self.__right(local),
                self.__top(local),
                self.__bottom(local)
            )