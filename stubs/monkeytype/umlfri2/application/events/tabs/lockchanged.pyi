from umlfri2.application.tab import Tab


class TabLockStatusChangedEvent:
    def __init__(self, tab: Tab) -> None: ...
    @property
    def tab(self) -> Tab: ...
