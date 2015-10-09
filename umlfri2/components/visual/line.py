from ..expressions import ConstantExpression
from .hbox import HBox
from umlfri2.types.color import Color
from .visualcomponent import VisualComponent
from .vbox import VBox


class Line(VisualComponent):
    def __init__(self, type: id='auto', color: Color=None):
        super().__init__(())
        self.__type = type
        self.__color = color or ConstantExpression(Color.get_color("black"))
    
    def __get_type(self):
        if self.__type == 'auto':
            parent = self._get_parent()
            while parent is not None:
                if isinstance(parent, VBox):
                    return 'horizontal'
                elif isinstance(parent, HBox):
                    return 'vertical'
            return 'horizontal'
        return self.__type
    
    def is_resizable(self, context):
        type = self.__get_type()
        return type == 'horizontal', type == 'vertical'
    
    def get_size(self, context, ruler):
        if self.__get_type() == 'horizontal':
            return 0, 1
        else:
            return 1, 0
    
    def draw(self, context, canvas, bounds, shadow=None):
        (x, y, w, h), (w_inner, h_inner) = self._compute_bounds(context, canvas.get_ruler(), bounds)
        
        color = shadow or self.__color(context)
        
        if self.__get_type() == 'horizontal':
            canvas.draw_line((x, y), (x + w, y), color)
        else:
            canvas.draw_line((x, y), (x, y + h), color)
