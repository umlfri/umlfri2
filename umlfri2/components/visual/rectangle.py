from umlfri2.components.expressions import NoneExpression, ConstantExpression
from umlfri2.ufl.types import UflColorType
from .visualcomponent import VisualComponent, VisualObject
from umlfri2.types.geometry import Rectangle, Point, Vector


class RectangleObject(VisualObject):
    def __init__(self, child, fill, border):
        self.__child = child
        self.__fill = fill
        self.__border = border
        self.__rectangle = None
        
        self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        self.__rectangle = bounds
        
        self.__child.assign_bounds(bounds)
    
    def get_minimal_size(self):
        return self.__child_size
    
    def draw(self, canvas, shadow):
        if shadow:
            canvas.draw_rectangle(
                Rectangle.from_point_size(
                    self.__rectangle.top_left + shadow.shift,
                    self.__rectangle.size,
                ),
                None,
                shadow.color
            )
        else:
            canvas.draw_rectangle(self.__rectangle, self.__border, self.__fill)
            self.__child.draw(canvas, None)


class RectangleComponent(VisualComponent):
    ATTRIBUTES = {
        'fill': UflColorType(),
        'border': UflColorType(),
    }
    
    def __init__(self, children, fill=None, border=None):
        super().__init__(children)
        self.__fill = fill or ConstantExpression(None, UflColorType())
        self.__border = border or ConstantExpression(None, UflColorType())
    
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            return RectangleObject(
                child._create_object(local, ruler),
                self.__fill(local),
                self.__border(local)
            )
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            fill=self.__fill,
            border=self.__border,
        )
        
        self._compile_children(variables)
