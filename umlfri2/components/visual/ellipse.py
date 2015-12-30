from umlfri2.components.expressions import ConstantExpression
from umlfri2.types.geometry import Rectangle, Size
from umlfri2.ufl.types import UflColorType
from .visualcomponent import VisualObject, VisualComponent


class EllipseObject(VisualObject):
    def __init__(self, child, fill, border):
        self.__child = child
        self.__fill = fill
        self.__border = border
        self.__rectangle = None
        
        if child is None:
            self.__child_size = Size(0, 0)
        else:
            self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        self.__rectangle = bounds
        
        if self.__child is not None:
            self.__child.assign_bounds(bounds)
    
    def get_minimal_size(self):
        return self.__child_size
    
    def draw(self, canvas, shadow):
        if shadow:
            canvas.draw_ellipse(
                Rectangle.from_point_size(
                    self.__rectangle.top_left + shadow.shift,
                    self.__rectangle.size,
                ),
                None,
                shadow.color
            )
        else:
            canvas.draw_ellipse(self.__rectangle, self.__border, self.__fill)
            if self.__child is not None:
                self.__child.draw(canvas, None)
    
    def is_resizable(self):
        if self.__child is None:
            return False, False
        else:
            return self.__child.is_resizable()


class EllipseComponent(VisualComponent):
    ATTRIBUTES = {
        'fill': UflColorType(),
        'border': UflColorType()
    }
    
    def __init__(self, children, fill=None, border=None):
        super().__init__(children)
        self.__fill = fill or ConstantExpression(None, UflColorType())
        self.__border = border or ConstantExpression(None, UflColorType())
    
    def _create_object(self, context, ruler):
        found_child = None
        for local, child in self._get_children(context):
            found_child = child._create_object(local, ruler)
            break
        
        return EllipseObject(found_child, self.__fill(context), self.__border(context))
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            fill=self.__fill,
            border=self.__border,
        )
        
        self._compile_children(variables)
