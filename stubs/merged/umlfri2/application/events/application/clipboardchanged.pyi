from ..base import Event as Event
from umlfri2.application.snippet.snippet import Snippet


class ClipboardSnippetChangedEvent(Event):
    def __init__(self, new_snippet: Snippet) -> None: ...
    @property
    def new_snippet(self) -> Snippet: ...
