import math
from .connectionlinecomponent import ConnectionLineComponent, ConnectionLineObject
from ..expressions import ConstantExpression, NoneExpression
from umlfri2.types.color import Colors
from umlfri2.types.geometry import Transformation
from umlfri2.ufl.types import UflColorType, UflProportionType, UflDefinedEnumType


class ArrowDefinition:
    def __init__(self, id, path, center, rotation):
        self.__id = id
        self.__path = path\
            .transform(
                Transformation.make_translate(-center.as_vector())
                * Transformation.make_rotation(-rotation)
            )
    
    @property
    def id(self):
        return self.__id
    
    @property
    def path(self):
        return self.__path


class ArrowObject(ConnectionLineObject):
    def __init__(self, position, style, color):
        self.__style = style
        self.__position = position
        self.__color = color
        self.__path = None
    
    def assign_points(self, points):
        pos = self._compute_position(points, self.__position)
        
        #self.__path = self.__style.path.transform(
        #    Transformation.make_translate(pos.position.as_vector())
        #)
        self.__path = self.__style.path.transform(
            Transformation.make_translate(pos.position.as_vector())
            * Transformation.make_rotation(-pos.orientation)
        )
    
    def draw(self, canvas):
        canvas.draw_path(self.__path, self.__color)


class ArrowComponent(ConnectionLineComponent):
    ATTRIBUTES = {
        'position': UflProportionType(),
        'style': UflDefinedEnumType(ArrowDefinition),
        'color': UflColorType(),
    }
    HAS_CHILDREN = False
    
    def __init__(self, position, style, color=None, fill=None):
        super().__init__(())
        self.__position = position
        self.__style = style
        self.__color = color or ConstantExpression(Colors.black)
        self.__fill = fill or NoneExpression
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            position=self.__position,
            style=self.__style,
            color=self.__color,
        )
    
    def _create_object(self, context):
        return ArrowObject(self.__position(context), self.__style(context), self.__color(context))
