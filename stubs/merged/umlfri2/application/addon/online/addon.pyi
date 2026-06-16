from _typeshed import Incomplete
from collections.abc import Generator
from typing import (
    List,
    Optional,
)
from umlfri2.application.addon.license.common import CommonLicense
from umlfri2.application.addon.local.addon import AddOn
from umlfri2.application.addon.online.version import OnlineAddOnVersion
from umlfri2.application.application import Application
from umlfri2.types.image import Image


class OnlineAddOn:
    def __init__(
        self,
        application: Application,
        identifier: str,
        versions: List[OnlineAddOnVersion]
    ) -> None: ...
    @property
    def identifier(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def author(self) -> str: ...
    @property
    def homepage(self) -> str: ...
    @property
    def license(self) -> CommonLicense: ...
    @property
    def icon(self) -> Image: ...
    @property
    def description(self) -> str: ...
    @property
    def requirements(self) -> Generator[Incomplete, Incomplete]: ...
    @property
    def provisions(self) -> Generator[Incomplete, Incomplete]: ...
    @property
    def versions(self) -> Generator[Incomplete, Incomplete]: ...
    @property
    def latest_version(self) -> OnlineAddOnVersion: ...
    @property
    def local_addon(self) -> Optional[AddOn]: ...
