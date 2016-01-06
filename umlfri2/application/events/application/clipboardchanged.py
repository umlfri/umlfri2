from ..base import Event


class ClipboardSnippetChangedEvent(Event):
    def __init__(self, new_snippet):
        self.__new_snippet = new_snippet
    
    @property
    def new_snippet(self):
        return self.__new_snippet
