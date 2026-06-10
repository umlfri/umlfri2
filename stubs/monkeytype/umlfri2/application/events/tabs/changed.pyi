from typing import Optional
from umlfri2.application.tab import Tab


class ChangedCurrentTabEvent:
    def __init__(self, tab: Optional[Tab]) -> None: ...
    @property
    def tab(self) -> Optional[Tab]: ...
