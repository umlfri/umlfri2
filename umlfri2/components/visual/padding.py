from ..expressions import ConstantExpression
from umlfri2.types.geometry import Rectangle, Size
from umlfri2.ufl.types import UflIntegerType
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
        self.__child.assign_bounds(
            Rectangle(
                bounds.x1 + self.__left,
                bounds.y1 + self.__top,
                bounds.width - self.__left - self.__right,
                bounds.height - self.__top - self.__bottom
            )
        )
    
    def get_minimal_size(self):
        return Size(self.__child_size.width + self.__left + self.__right,
                    self.__child_size.height + self.__top + self.__bottom)
    
    def draw(self, canvas, shadow):
        self.__child.draw(canvas, shadow)


class PaddingComponent(VisualComponent):
    ATTRIBUTES = {
        'padding': UflIntegerType(),
        'left': UflIntegerType(),
        'right': UflIntegerType(),
        'top': UflIntegerType(),
        'bottom': UflIntegerType(),
    }
    
    def __init__(self, children, padding=None, left=None, right=None, top=None, bottom=None):
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
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            left=self.__left,
            right=self.__right,
            top=self.__top,
            bottom=self.__bottom,
        )
        
        self._compile_children(variables)
