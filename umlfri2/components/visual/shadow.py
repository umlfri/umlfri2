from umlfri2.components.expressions import ConstantExpression
from umlfri2.types.color import Color
from .visualcomponent import VisualComponent, VisualObject


class ShadowObject(VisualObject):
    def __init__(self, child, color, padding):
        self.__child = child
        self.__color = color
        self.__padding = padding
        self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        x, y, w, h = bounds
        self.__child.assign_bounds((x, y, w - self.__padding, h - self.__padding))
    
    def get_minimal_size(self):
        w, h = self.__child_size
        return w + self.__padding, h + self.__padding
    
    def draw(self, canvas, shadow, shadow_shift):
        self.__child.draw(canvas, self.__color, self.__padding)
        self.__child.draw(canvas, None, None)


class Shadow(VisualComponent):
    def __init__(self, children, color: Color=None, padding: int=None):
        super().__init__(children)
        self.__color = color or ConstantExpression(Color.get_color("lightgray"))
        self.__padding = padding or ConstantExpression(5)
    
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            return ShadowObject(
                child._create_object(local, ruler),
                self.__color(local),
                self.__padding(local)
            )
