from typing import List
from umlfri2.application.tab import Tab
from umlfri2.datalayer.storages.zip import ZipStorage


class LockedTabsSaver:
    def __init__(self, storage: ZipStorage, path: str) -> None: ...
    def save(self, locked_tabs: List[Tab]) -> None: ...
