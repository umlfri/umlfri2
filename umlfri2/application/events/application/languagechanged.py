from __future__ import annotations

from typing import Optional

from ..base import Event


class LanguageChangedEvent(Event):
    def __init__(self, language: Optional[str]) -> None:
        self.__language = language
    
    @property
    def language(self) -> Optional[str]:
        return self.__language
