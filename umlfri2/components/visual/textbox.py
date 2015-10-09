from ..expressions import ConstantExpression
from ..text import TextContainer, Text
from umlfri2.types.color import Color
from umlfri2.types.font import Font
from .visualcomponent import VisualComponent


class TextBox(VisualComponent):
    def __init__(self, children, text: str=None, color: Color=None, font: Font=None):
        super().__init__(())
        self.__color = color or ConstantExpression(Color.get_color("black"))
        self.__font = font or ConstantExpression(Font("Arial", 10))
        if text is None:
            self.__text = TextContainer(children)
        else:
            self.__text = Text(text)
    
    def is_resizable(self, context):
        return False, False
    
    def get_size(self, context, ruler):
        text = self.__text.get_text(context)
        return ruler.measure_text(self.__font(context), text)
    
    def draw(self, context, canvas, bounds, shadow=None):
        x, y, w, h = bounds
        
        color = shadow or self.__color(context)
        text = self.__text.get_text(context)
        
        canvas.draw_text((x, y), text, self.__font, color)
