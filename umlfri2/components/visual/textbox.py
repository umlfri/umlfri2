from ..expressions import ConstantExpression
from ..text import TextContainer, Text
from umlfri2.types.color import Color
from umlfri2.types.font import Font
from umlfri2.ufl.types import UflStringType, UflColorType, UflFontType
from .visualcomponent import VisualComponent, VisualObject


class TextBoxObject(VisualObject):
    def __init__(self, size, text, color, font):
        self.__size = size
        self.__text = text
        self.__color = color
        self.__font = font
        self.__position = None
    
    def assign_bounds(self, bounds):
        self.__position = bounds[0], bounds[1]
    
    def get_minimal_size(self):
        return self.__size
    
    def draw(self, canvas, shadow):
        if shadow:
            x, y = self.__position
            canvas.draw_text(
                (x + shadow.shift, y + shadow.shift),
                self.__text,
                self.__font,
                shadow.color
            )
        else:
            canvas.draw_text(self.__position, self.__text, self.__font, self.__color)


class TextBox(VisualComponent):
    ATTRIBUTES = {
        'text': UflStringType,
        'color': UflColorType,
        'font': UflFontType,
    }
    
    def __init__(self, children, text=None, color=None, font=None):
        super().__init__(())
        self.__color = color or ConstantExpression(Color.get_color("black"))
        self.__font = font or ConstantExpression(Font("Arial", 10))
        if text is None:
            self.__text = TextContainer(children)
        else:
            self.__text = Text(text)
    
    def is_resizable(self, context):
        return False, False
    
    def _create_object(self, context, ruler):
        text = self.__text.get_text(context)
        font = self.__font(context)
        color = self.__color(context)
        size = ruler.measure_text(font, text)
        
        return TextBoxObject(size, text, color, font)
