from umlfri2.application.addon.local.addon import AddOn
from umlfri2.application.addon.local.manager import AddOnManager


class AddOnUninstaller:
    def __init__(
        self,
        manager: AddOnManager,
        addon: AddOn
    ) -> None: ...
    def do(self) -> None: ...
    @property
    def finished(self) -> bool: ...
    @property
    def has_error(self) -> bool: ...
