from umlfri2.application import Application as Application
from umlfri2.application.events.application import ClipboardSnippetChangedEvent as ClipboardSnippetChangedEvent
from umlfri2.application.snippet import Snippet as Snippet

class QtClipboardAdatper:
    UMLFRI_CLIPBOARD_FORMAT: str
    def __init__(self) -> None: ...
