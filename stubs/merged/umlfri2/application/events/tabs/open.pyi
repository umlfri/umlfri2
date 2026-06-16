from ..base import Event as Event
from umlfri2.application.tab import Tab


class OpenTabEvent(Event):
    def __init__(self, tab: Tab) -> None: ...
    @property
    def tab(self) -> Tab: ...
