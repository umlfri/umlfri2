from .connectionlinecomponent import ConnectionLineComponent, ConnectionLineObject
from ..expressions import ConstantExpression
from umlfri2.components.visual.canvas import LineStyle
from umlfri2.types.color import Colors
from umlfri2.types.geometry import PathBuilder
from umlfri2.ufl.types import UflColorType, UflProportionType, UflTypedEnumType


class LineObject(ConnectionLineObject):
    def __init__(self, start, end, style, color):
        self.__start = start
        self.__end = end
        self.__style = style
        self.__color = color
        self.__path = None
        
    def assign_points(self, points):
        p1 = self._compute_position(points, self.__start)
        p2 = self._compute_position(points, self.__end)
        
        path = PathBuilder()
        path.move_to(p1.position)
        for point in points[p1.id + 1:p2.id + 1]:
            path.line_to(point)
        path.line_to(p2.position)
    
    def draw(self, canvas):
        canvas.draw_path(self.__path, self.__color, line_style=self.__style)


class LineComponent(ConnectionLineComponent):
    ATTRIBUTES = {
        'start': UflProportionType(),
        'end': UflProportionType(),
        'style': UflTypedEnumType(LineStyle),
        'color': UflColorType(),
    }
    HAS_CHILDREN = False
    
    def __init__(self, start=None, end=None, style=None, color=None):
        super().__init__(())
        self.__start = start or ConstantExpression(0, UflProportionType())
        self.__end = end or ConstantExpression(1, UflProportionType())
        self.__style = style or ConstantExpression(LineStyle.solid, UflTypedEnumType(LineStyle))
        self.__color = color or ConstantExpression(Colors.black)
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            start=self.__start,
            end=self.__end,
            style=self.__style,
            color=self.__color,
        )
    
    def _create_object(self, context):
        return LineObject(self.__start(context), self.__end(context), self.__style(context), self.__color(context))
