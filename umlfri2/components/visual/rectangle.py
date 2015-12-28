from umlfri2.components.expressions import NoneExpression, ConstantExpression
from umlfri2.ufl.types import UflColorType, UflDefinedEnumType
from .visualcomponent import VisualComponent, VisualObject
from umlfri2.types.geometry import Rectangle, Point, Vector


class CornerDefinition:
    def __init__(self, id, path, start, end, center, corner):
        self.__id = id
    
    @property
    def id(self):
        return self.__id


class SideDefinition:
    def __init__(self, id, path, start, end, center, side):
        self.__id = id
    
    @property
    def id(self):
        return self.__id


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
    
    def is_resizable(self):
        return self.__child.is_resizable()


class RectangleComponent(VisualComponent):
    ATTRIBUTES = {
        'fill': UflColorType(),
        'border': UflColorType(),
        'topleft': UflDefinedEnumType(CornerDefinition),
        'topright': UflDefinedEnumType(CornerDefinition),
        'bottomleft': UflDefinedEnumType(CornerDefinition),
        'bottomright': UflDefinedEnumType(CornerDefinition),
        'left': UflDefinedEnumType(SideDefinition),
        'right': UflDefinedEnumType(SideDefinition),
        'top': UflDefinedEnumType(SideDefinition),
        'bottom': UflDefinedEnumType(SideDefinition)
    }
    
    # TODO: rounded rectangle
    def __init__(self, children, fill=None, border=None, topleft=None, topright=None, bottomleft=None, bottomright=None,
                 left=None, right=None, top=None, bottom=None):
        super().__init__(children)
        self.__fill = fill or ConstantExpression(None, UflColorType())
        self.__border = border or ConstantExpression(None, UflColorType())
        
        if left and (topleft or bottomleft):
            raise Exception
        
        if right and (topright or bottomright):
            raise Exception
        
        if top and (topleft or topright):
            raise Exception
        
        if bottom and (bottomleft or bottomright):
            raise Exception
        
        self.__topleft = topleft
        self.__topright = topright
        self.__bottomleft = bottomleft
        self.__bottomright = bottomright
        self.__left = left
        self.__right = right
        self.__top = top
        self.__bottom = bottom
    
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            return RectangleObject(
                child._create_object(local, ruler),
                self.__fill(context),
                self.__border(context)
            )
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            fill=self.__fill,
            border=self.__border,
        )
        
        self._compile_children(variables)
