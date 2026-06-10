from umlfri2.application.tab import Tab
from umlfri2.datalayer.storages.zip import ZipStorage
from umlfri2.qtgui.rendering.qtruler import QTRuler


class WholeSolutionSaver:
    def __init__(
        self,
        storage: ZipStorage,
        ruler: QTRuler
    ) -> None: ...
    def add_locked_tab(self, tab: Tab) -> None: ...
    def save(self) -> None: ...
