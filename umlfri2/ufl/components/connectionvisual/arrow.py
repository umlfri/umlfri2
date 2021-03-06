import math

from umlfri2.types.enums import ArrowOrientation
from .connectionvisualcomponent import ConnectionVisualComponent, ConnectionVisualObject
from ..valueproviders import DefaultValueProvider
from umlfri2.types.color import Colors
from umlfri2.types.geometry import Transformation
from umlfri2.ufl.types.complex import UflColorType, UflProportionType
from umlfri2.ufl.types.enum import UflDefinedEnumType, UflTypedEnumType
from umlfri2.ufl.types.structured import UflNullableType


class ArrowDefinition:
    def __init__(self, id, path, center, rotation):
        self.__id = id
        self.__path = path\
            .transform(
                Transformation.make_translate(-center.as_vector())
                # transformation is clock-wise, given rotation is counter-clockwise
                * Transformation.make_rotation(-(-rotation))
            )
    
    @property
    def id(self):
        return self.__id
    
    @property
    def path(self):
        return self.__path


class ConnectionArrowObject(ConnectionVisualObject):
    def __init__(self, position, style, orientation, color, fill):
        self.__style = style
        self.__position = position
        self.__orientation = orientation
        self.__color = color
        self.__fill = fill
        self.__path = None
    
    def assign_points(self, points):
        pos = self._compute_position(points, self.__position)
        
        transformation = Transformation.make_translate(pos.position.as_vector())
        
        if self.__orientation == ArrowOrientation.source:
            transformation *= Transformation.make_rotation(math.pi)
        
        transformation *= Transformation.make_rotation(pos.orientation)
        
        self.__path = self.__style.path.transform(transformation)
    
    def draw(self, canvas):
        canvas.draw_path(self.__path, self.__color, self.__fill)


class ConnectionArrowComponent(ConnectionVisualComponent):
    ATTRIBUTES = {
        'position': UflProportionType(),
        'style': UflDefinedEnumType(ArrowDefinition),
        'orientation': UflTypedEnumType(ArrowOrientation),
        'color': UflColorType(),
        'fill': UflNullableType(UflColorType()),
    }
    HAS_CHILDREN = False
    
    def __init__(self, position, style, orientation=None, color=None, fill=None):
        super().__init__(())
        self.__position = position
        self.__orientation = orientation or DefaultValueProvider(ArrowOrientation.destination)
        self.__style = style
        self.__color = color or DefaultValueProvider(Colors.black)
        self.__fill = fill or DefaultValueProvider(None)
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            position=self.__position,
            orientation=self.__orientation,
            style=self.__style,
            color=self.__color,
            fill=self.__fill,
        )
    
    def _create_object(self, context):
        return ConnectionArrowObject(self.__position(context).value, self.__style(context), self.__orientation(context),
                                     self.__color(context), self.__fill(context))
