from collections import namedtuple
from umlfri2.components.expressions import ConstantExpression
from umlfri2.types.color import Color
from umlfri2.types.geometry import Size, Rectangle, Vector
from umlfri2.ufl.types import UflColorType, UflIntegerType
from .visualcomponent import VisualComponent, VisualObject


ShadowInfo = namedtuple('ShadowInfo', ('color', 'shift'))


class ShadowObject(VisualObject):
    def __init__(self, child, color, padding):
        self.__child = child
        self.__color = color
        self.__padding = padding
        self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        self.__child.assign_bounds(bounds)
    
    def get_minimal_size(self):
        return self.__child_size
    
    def draw(self, canvas, shadow):
        self.__child.draw(canvas, ShadowInfo(self.__color,
                                             Vector(self.__padding, self.__padding)))
        self.__child.draw(canvas, None)


class ShadowComponent(VisualComponent):
    ATTRIBUTES = {
        'color': UflColorType(),
        'padding': UflIntegerType(),
    }
    
    def __init__(self, children, color=None, padding=None):
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
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            color=self.__color,
            padding=self.__padding,
        )
        
        self._compile_children(variables)
