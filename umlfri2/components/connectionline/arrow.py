from .connectionlinecomponent import ConnectionLineComponent, ConnectionLineObject
from ..expressions import ConstantExpression, NoneExpression
from umlfri2.types.color import Colors
from umlfri2.ufl.types import UflColorType, UflStringType, UflProportionType


class ArrowObject(ConnectionLineObject):
    def __init__(self, position, style, color):
        pass # TODO: finish this
    
    def assign_points(self, points):
        pass
    
    def draw(self, canvas):
        pass


class Arrow(ConnectionLineComponent):
    ATTRIBUTES = {
        'position': UflProportionType(),
        'style': UflStringType(),
        'color': UflColorType(),
    }
    HAS_CHILDREN = False
    
    def __init__(self, position, style, size=None, color=None, fill=None):
        super().__init__(())
        self.__position = position
        self.__style = style
        self.__size = size or ConstantExpression(10)
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
        return Arrow(self.__position(context), self.__style(context), self.__color(context))
