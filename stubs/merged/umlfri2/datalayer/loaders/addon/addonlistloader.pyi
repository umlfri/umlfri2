from ...constants import ADDON_ADDON_FILE as ADDON_ADDON_FILE
from .addoninfoloader import AddOnInfoLoader as AddOnInfoLoader
from .addonloader import AddOnLoader as AddOnLoader
from _typeshed import Incomplete
from collections.abc import Generator

class AddOnListLoader:
    def __init__(self, application, storage, system_location) -> None: ...
    def load_all(self) -> Generator[Incomplete]: ...
    def install_from(self, storage, online_addon_version): ...
