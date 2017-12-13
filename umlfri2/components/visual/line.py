from umlfri2.types.enums import LineOrientation
from umlfri2.types.threestate import Maybe
from ..expressions import ConstantExpression
from .hbox import HBoxComponent
from umlfri2.types.color import Colors
from umlfri2.types.geometry import Size
from umlfri2.ufl.types import UflTypedEnumType, UflColorType
from .visualcomponent import VisualComponent, VisualObject
from .vbox import VBoxComponent


class LineObject(VisualObject):
    def __init__(self, orientation, color):
        self.__orientation = orientation
        self.__color = color
        self.__point1 = None
        self.__point2 = None
    
    def assign_bounds(self, bounds):
        self.__point1 = bounds.top_left
        
        if self.__orientation == LineOrientation.horizontal:
            self.__point2 = bounds.top_right
        else:
            self.__point2 = bounds.bottom_left
    
    def get_minimal_size(self):
        if self.__orientation == LineOrientation.vertical:
            return Size(0, 1)
        else:
            return Size(1, 0)
            
    def draw(self, canvas, shadow):
        if shadow:
            canvas.draw_line(
                self.__point1 + shadow.shift,
                self.__point2 + shadow.shift,
                shadow.color
            )
        else:
            canvas.draw_line(self.__point1, self.__point2, self.__color)
    
    def is_resizable(self):
        if self.__orientation == LineOrientation.horizontal:
            return Maybe, False
        else:
            return False, Maybe


class LineComponent(VisualComponent):
    ATTRIBUTES = {
        'orientation': UflTypedEnumType(LineOrientation),
        'color': UflColorType(),
    }
    HAS_CHILDREN = False
    
    def __init__(self, orientation=None, color=None):
        super().__init__(())
        self.__orientation = orientation or ConstantExpression(LineOrientation.auto, UflTypedEnumType(LineOrientation))
        self.__color = color or ConstantExpression(Colors.black)
    
    def __get_orientation(self, context):
        orientation = self.__orientation(context)
        
        if orientation == LineOrientation.auto:
            parent = self._get_parent()
            while parent is not None:
                if isinstance(parent, VBoxComponent):
                    return LineOrientation.horizontal
                elif isinstance(parent, HBoxComponent):
                    return LineOrientation.vertical
                parent = parent._get_parent()
            return LineOrientation.horizontal
        return orientation
    
    def _create_object(self, context, ruler):
        return LineObject(self.__get_orientation(context), self.__color(context))
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            orientation=self.__orientation,
            color=self.__color,
        )
