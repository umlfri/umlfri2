from umlfri2.application.snippet.snippet import Snippet


class ClipboardSnippetChangedEvent:
    def __init__(self, new_snippet: Snippet) -> None: ...
    @property
    def new_snippet(self) -> Snippet: ...
