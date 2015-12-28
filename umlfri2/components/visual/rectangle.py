import math

from umlfri2.components.expressions import NoneExpression, ConstantExpression
from umlfri2.ufl.types import UflColorType, UflDefinedEnumType
from .visualcomponent import VisualComponent, VisualObject
from umlfri2.types.geometry import Rectangle, Transformation, PathBuilder


class CornerDefinition:
    def __init__(self, id, path, ornament, center, corner):
        self.__id = id
        
        if corner == 'top left':
            rotation = 0
        elif corner == 'top right':
            rotation = math.pi / 2
        elif corner == 'bottom right':
            rotation = math.pi
        else:
            rotation = -math.pi / 2
        
        if len(path.segments) > 1:
            raise Exception("Corner path can have only one segment (corner '{0}')".format(id))
        
        transformation = Transformation.make_translate(-center.as_vector()) * Transformation.make_rotation(-rotation)
        
        self.__path = path.transform(transformation)
        if ornament is None:
            self.__ornament = None
        else:
            self.__ornament = ornament.transform(transformation)
    
    @property
    def id(self):
        return self.__id
    
    @property
    def path(self):
        return self.__path
    
    @property
    def ornament(self):
        return self.__ornament


class SideDefinition:
    def __init__(self, id, path, center, side):
        self.__id = id
    
    @property
    def id(self):
        return self.__id


class RoundedRectangleObject(VisualObject):
    def __init__(self, child, fill, border, corners):
        self.__child = child
        self.__fill = fill
        self.__border = border
        self.__path = None
        self.__ornaments_path = None
        self.__corners = corners
        
        self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        corners = [
            (bounds.top_left, 0, self.__corners[0]),
            (bounds.top_right, -math.pi / 2, self.__corners[1]),
            (bounds.bottom_right, math.pi, self.__corners[2]),
            (bounds.bottom_left, math.pi / 2, self.__corners[3])
        ]
        
        path = PathBuilder()
        ornaments = PathBuilder()
        
        for point, rotation, corner in corners:
            if corner is None:
                path.move_or_line_to(point)
            else:
                transformation = Transformation.make_translate(point) * Transformation.make_rotation(rotation)
                path.from_path(corner.path.transform(transformation), True)
                if corner.ornament is not None:
                    ornaments.from_path(corner.ornament.transform(transformation))
        
        path.close()
        
        self.__path = path.build()
        self.__ornaments_path = ornaments.build()
        
        self.__child.assign_bounds(bounds)
    
    def get_minimal_size(self):
        return self.__child_size
    
    def draw(self, canvas, shadow):
        if shadow:
            canvas.draw_path(
                self.__path.transform(Transformation.make_translate(shadow.shift)),
                None,
                shadow.color
            )
        else:
            canvas.draw_path(self.__path, self.__border, self.__fill)
            canvas.draw_path(self.__ornaments_path, self.__border, None)
            self.__child.draw(canvas, None)
    
    def is_resizable(self):
        return self.__child.is_resizable()


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
        
        if topleft or topright or bottomleft or bottomright:
            self.__corners = (topleft or NoneExpression, topright or NoneExpression,
                              bottomright or NoneExpression, bottomleft or NoneExpression)
        else:
            self.__corners = None
        
        if top or right or bottom or left:
            self.__sides = (left or NoneExpression, top or NoneExpression,
                            right or NoneExpression, bottom or NoneExpression)
        else:
            self.__sides = None
    
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            if self.__corners or self.__sides:
                return RoundedRectangleObject(
                    child._create_object(local, ruler),
                    self.__fill(context),
                    self.__border(context),
                    [corner(context) for corner in self.__corners]
                )
            else:
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
