from .addon import OnlineAddOn as OnlineAddOn
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.constants.paths import ONLINE_ADDONS as ONLINE_ADDONS
from umlfri2.datalayer.loaders.onlineaddons import OnlineAddOnListLoader as OnlineAddOnListLoader
from umlfri2.datalayer.savers import OnlineAddOnListSaver as OnlineAddOnListSaver
from umlfri2.datalayer.storages import DirectoryStorage as DirectoryStorage, ZipStorage as ZipStorage

update_executor: Incomplete

class OnlineAddOnManager:
    def __init__(self, application) -> None: ...
    def update(self) -> None: ...
    def __iter__(self): ...
    @property
    def updated_addons(self) -> Generator[Incomplete]: ...
