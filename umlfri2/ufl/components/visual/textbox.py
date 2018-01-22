from ..valueproviders import DefaultValueProvider
from ..text import TextContainerComponent, TextDataComponent
from umlfri2.types.color import Colors
from umlfri2.types.font import Fonts
from umlfri2.types.geometry import Point
from umlfri2.ufl.types import UflStringType, UflColorType, UflFontType
from ..base.componenttype import ComponentType
from .visualcomponent import VisualComponent, VisualObject


class TextBoxObject(VisualObject):
    def __init__(self, size, text, color, font):
        self.__size = size
        self.__text = text
        self.__color = color
        self.__font = font
        self.__position = None
    
    def assign_bounds(self, bounds):
        self.__position = bounds.top_left
    
    def get_minimal_size(self):
        return self.__size
    
    def draw(self, canvas, shadow):
        if shadow:
            canvas.draw_text(
                self.__position + shadow.shift,
                self.__text,
                self.__font,
                shadow.color
            )
        else:
            canvas.draw_text(self.__position, self.__text, self.__font, self.__color)
    
    def is_resizable(self):
        return False, False


class TextBoxComponent(VisualComponent):
    ATTRIBUTES = {
        'text': UflStringType(),
        'color': UflColorType(),
        'font': UflFontType(),
    }
    CHILDREN_TYPE = ComponentType.text
    
    def __init__(self, children, text=None, color=None, font=None):
        super().__init__(())
        self.__color = color or DefaultValueProvider(Colors.black)
        self.__font = font or DefaultValueProvider(Fonts.default)
        if text is None:
            self.__text = TextContainerComponent(children)
        else:
            self.__text = TextDataComponent(text)
    
    def _create_object(self, context, ruler):
        text = self.__text.get_text(context)
        font = self.__font(context)
        color = self.__color(context)
        size = ruler.measure_text(font, text)
        
        return TextBoxObject(size, text, color, font)
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            color=self.__color,
            font=self.__font,
        )
        
        self.__text.compile(type_context)
