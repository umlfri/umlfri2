from __future__ import annotations

from typing import Any

from ..base import Event


class ItemSelectedEvent(Event):
    """
    Item selected in the project tree.
    """
    
    def __init__(self, item: Any) -> None:
        self.__item = item
    
    @property
    def item(self) -> Any:
        return self.__item
