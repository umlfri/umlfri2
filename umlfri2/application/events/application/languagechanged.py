from ..base import Event


class LanguageChangedEvent(Event):
    def __init__(self, language):
        self.__language = language
    
    @property
    def language(self):
        return self.__language
