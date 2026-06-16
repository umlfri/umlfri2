from .actions import AddOnStarter as AddOnStarter, AddOnStopper as AddOnStopper
from .state import AddOnState as AddOnState
from umlfri2.application.events.addon import AddOnInstalledEvent as AddOnInstalledEvent, AddOnUninstalledEvent as AddOnUninstalledEvent, AddOnUpdatedEvent as AddOnUpdatedEvent
from umlfri2.constants.paths import ADDONS as ADDONS, LOCAL_ADDONS as LOCAL_ADDONS
from umlfri2.datalayer.loaders import AddOnListLoader as AddOnListLoader
from umlfri2.datalayer.storages import DirectoryStorage as DirectoryStorage
from typing import (
    Iterator,
    Optional,
)
from umlfri2.application.addon.local.actions.starter import AddOnStarter
from umlfri2.application.addon.local.actions.stopper import AddOnStopper
from umlfri2.application.addon.local.addon import AddOn
from umlfri2.application.addon.online.version import OnlineAddOnVersion
from umlfri2.application.application import Application
from umlfri2.datalayer.storages.zip import ZipStorage


class AddOnManager:
    def __init__(self, application: Application) -> None: ...
    def load_addons(self) -> None: ...
    def install_addon(
        self,
        storage: ZipStorage,
        online_addon_version: OnlineAddOnVersion
    ) -> AddOn: ...
    def install_addon_update(self, storage, online_addon_version): ...
    def uninstall_addon(self, addon: AddOn) -> None: ...
    def get_addon(self, identifier: str) -> Optional[AddOn]: ...
    def start_all(self) -> AddOnStarter: ...
    def stop_all(self) -> AddOnStopper: ...
    def __iter__(self) -> Iterator[AddOn]: ...
