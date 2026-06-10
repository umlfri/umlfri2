from umlfri2.application.addon.local.manager import AddOnManager
from umlfri2.application.addon.online.version import OnlineAddOnVersion


class OnlineAddOnInstaller:
    def __init__(
        self,
        local_manager: AddOnManager,
        addon_version: OnlineAddOnVersion
    ) -> None: ...
    def do(self) -> None: ...
    @property
    def finished(self) -> bool: ...
    @property
    def has_error(self) -> bool: ...
