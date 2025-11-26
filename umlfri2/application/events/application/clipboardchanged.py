from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.snippet import Snippet


class ClipboardSnippetChangedEvent(Event):
    def __init__(self, new_snippet: Snippet) -> None:
        self.__new_snippet = new_snippet
    
    @property
    def new_snippet(self) -> Snippet:
        return self.__new_snippet
