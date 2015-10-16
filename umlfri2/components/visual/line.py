from ..expressions import ConstantExpression
from .hbox import HBox
from umlfri2.types.color import Color
from umlfri2.ufl.types import UflTypedEnumType, UflColorType
from .visualcomponent import VisualComponent, VisualObject
from .vbox import VBox


class LineOrientation:
    auto = 1,
    horizontal = 2
    vertical = 3


class LineObject(VisualObject):
    def __init__(self, orientation, color):
        self.__orientation = orientation
        self.__color = color
        self.__point1 = None
        self.__point2 = None
    
    def assign_bounds(self, bounds):
        self.__point1 = bounds[0], bounds[1]
        
        if self.__orientation == LineOrientation.horizontal:
            self.__point2 = bounds[0] + bounds[2], bounds[1]
        else:
            self.__point2 = bounds[0], bounds[1] + bounds[3]
    
    def get_minimal_size(self):
        if self.__orientation == LineOrientation.vertical:
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
        'orientation': UflTypedEnumType(LineOrientation),
        'color': UflColorType,
    }
    HAS_CHILDREN = False
    
    def __init__(self, orientation=None, color=None):
        super().__init__(())
        self.__orientation = orientation or ConstantExpression(LineOrientation.auto)
        self.__color = color or ConstantExpression(Color.get_color("black"))
    
    def __get_orientation(self, context):
        orientation = self.__orientation(context)
        
        if orientation == LineOrientation.auto:
            parent = self._get_parent()
            while parent is not None:
                if isinstance(parent, VBox):
                    return LineOrientation.horizontal
                elif isinstance(parent, HBox):
                    return LineOrientation.vertical
            return LineOrientation.horizontal
        return orientation
    
    def is_resizable(self, context):
        orientation = self.__get_orientation(context)
        return orientation == LineOrientation.horizontal, orientation == LineOrientation.vertical
    
    def _create_object(self, context, ruler):
        return LineObject(self.__get_orientation(context), self.__color(context))
