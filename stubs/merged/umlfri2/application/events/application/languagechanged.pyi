from ..base import Event as Event
from typing import Optional


class LanguageChangedEvent(Event):
    def __init__(self, language: Optional[str]) -> None: ...
    @property
    def language(self): ...
