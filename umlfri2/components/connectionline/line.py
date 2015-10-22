from .connectionlinecomponent import ConnectionLineComponent, ConnectionLineObject
from ..expressions import ConstantExpression
from umlfri2.components.visual.canvas import LineStyle
from umlfri2.types.color import Colors
from umlfri2.ufl.types import UflColorType, UflProportionType, UflTypedEnumType


class LineObject(ConnectionLineObject):
    def __init__(self, start, end, style, color):
        self.__start = start
        self.__end = end
        self.__style = style
        self.__color = color
        self.__points = []
        
    def assign_points(self, points):
        p1 = self._compute_position(points, self.__start)
        p2 = self._compute_position(points, self.__end)
        
        self.__points = []
        self.__points.append(p1.position)
        for point in points[p1.id + 1:p2.id + 1]:
            self.__points.append(point)
        self.__points.append(p2.position)
    
    def draw(self, canvas):
        old = None
        first = True
        
        for point in self.__points:
            if first:
                first = False
            else:
                canvas.draw_line(old, point, self.__color, 1, self.__style)
            
            old = point


class Line(ConnectionLineComponent):
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
        return Line(self.__start(context), self.__end(context), self.__style(context), self.__color(context))
