from ..base import Event as Event
from typing import Optional
from umlfri2.application.tab import Tab


class ChangedCurrentTabEvent(Event):
    def __init__(self, tab: Optional[Tab]) -> None: ...
    @property
    def tab(self) -> Optional[Tab]: ...
