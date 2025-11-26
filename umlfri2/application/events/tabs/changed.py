from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.tab import Tab


class ChangedCurrentTabEvent(Event):
    def __init__(self, tab: Optional[Tab]) -> None:
        self.__tab = tab
    
    @property
    def tab(self) -> Optional[Tab]:
        return self.__tab
