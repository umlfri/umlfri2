from .textcomponent import TextComponent


class Text(TextComponent):
    def __init__(self, text: str):
        super().__init__(())
        self.__text = text
    
    def get_text(self, context):
        return self.__text(context)
