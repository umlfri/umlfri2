from ..expressions import ConstantExpression
from .hbox import HBox
from umlfri2.types.color import Color
from umlfri2.ufl.types import UflEnumType, UflColorType
from .visualcomponent import VisualComponent, VisualObject
from .vbox import VBox


class LineObject(VisualObject):
    def __init__(self, type, color):
        self.__type = type
        self.__color = color
        self.__point1 = None
        self.__point2 = None
    
    def assign_bounds(self, bounds):
        self.__point1 = bounds[0], bounds[1]
        
        if self.__type == 'horizontal':
            self.__point2 = bounds[0] + bounds[2], bounds[1]
        else:
            self.__point2 = bounds[0], bounds[1] + bounds[3]
    
    def get_minimal_size(self):
        if self.__type == 'horizontal':
            return 0, 1
        else:
            return 1, 0
            
    def draw(self, canvas, shadow):
        if shadow:
            x1, y1 = self.__point1
            x2, y2 = self.__point2
            canvas.draw_line(
                (x1 + shadow.shift, y1 + shadow.shift),
                (x2 + shadow.shift, y2 + shadow.shift),
                shadow.color
            )
        else:
            canvas.draw_line(self.__point1, self.__point2, self.__color)

class Line(VisualComponent):
    ATTRIBUTES = {
        'type': UflEnumType(('auto', 'horizontal', 'vertical')),
        'color': UflColorType,
    }
    HAS_CHILDREN = False
    
    def __init__(self, type=None, color=None):
        super().__init__(())
        self.__type = type or ConstantExpression('auto')
        self.__color = color or ConstantExpression(Color.get_color("black"))
    
    def __get_type(self, context):
        type = self.__type(context)
        
        if type == 'auto':
            parent = self._get_parent()
            while parent is not None:
                if isinstance(parent, VBox):
                    return 'horizontal'
                elif isinstance(parent, HBox):
                    return 'vertical'
            return 'horizontal'
        return type
    
    def is_resizable(self, context):
        type = self.__get_type(context)
        return type == 'horizontal', type == 'vertical'
    
    def _create_object(self, context, ruler):
        return LineObject(self.__get_type(context), self.__color(context))
