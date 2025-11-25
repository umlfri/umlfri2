from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.tab import Tab


class TabLockStatusChangedEvent(Event):
    def __init__(self, tab: Tab) -> None:
        self.__tab = tab

    @property
    def tab(self) -> Tab:
        return self.__tab
