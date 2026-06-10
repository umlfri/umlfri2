from umlfri2.application.addon.online.version import OnlineAddOnVersion
from umlfri2.datalayer.storages.zip import ZipStorage


class OnlineAddonVersionDownloader:
    def __init__(self, version: OnlineAddOnVersion) -> None: ...
    @property
    def downloaded(self) -> bool: ...
    @property
    def storage(self) -> ZipStorage: ...
