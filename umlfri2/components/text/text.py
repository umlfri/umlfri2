from .textcomponent import TextComponent
from umlfri2.ufl.types import UflStringType


class Text(TextComponent):
    ATTRIBUTES = {
        'text': UflStringType,
    }
    
    HAS_CHILDREN = False
    
    def __init__(self, text):
        super().__init__(())
        self.__text = text
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            text=self.__text
        )
    
    def get_text(self, context):
        return self.__text(context)
