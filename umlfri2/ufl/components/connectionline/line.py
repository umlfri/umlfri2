from umlfri2.types.proportion import EMPTY_PROPORTION, WHOLE_PROPORTION
from .connectionlinecomponent import ConnectionVisualComponent, ConnectionVisualObject
from ..valueproviders import DefaultValueProvider
from umlfri2.types.enums import LineStyle
from umlfri2.types.color import Colors
from umlfri2.types.geometry import PathBuilder
from umlfri2.ufl.types import UflColorType, UflProportionType, UflTypedEnumType


class LineObject(ConnectionVisualObject):
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
        
        self.__path = path.build()
    
    def draw(self, canvas):
        canvas.draw_path(self.__path, self.__color, line_style=self.__style)


class VisualComponent(ConnectionVisualComponent):
    ATTRIBUTES = {
        'start': UflProportionType(),
        'end': UflProportionType(),
        'style': UflTypedEnumType(LineStyle),
        'color': UflColorType(),
    }
    HAS_CHILDREN = False
    
    def __init__(self, start=None, end=None, style=None, color=None):
        super().__init__(())
        self.__start = start or DefaultValueProvider(EMPTY_PROPORTION)
        self.__end = end or DefaultValueProvider(WHOLE_PROPORTION)
        self.__style = style or DefaultValueProvider(LineStyle.solid)
        self.__color = color or DefaultValueProvider(Colors.black)
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            start=self.__start,
            end=self.__end,
            style=self.__style,
            color=self.__color,
        )
    
    def _create_object(self, context):
        return LineObject(self.__start(context).value, self.__end(context).value, self.__style(context), self.__color(context))
