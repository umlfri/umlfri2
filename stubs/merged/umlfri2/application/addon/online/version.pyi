from .actions import OnlineAddOnInstaller as OnlineAddOnInstaller, OnlineAddOnUpdater as OnlineAddOnUpdater
from _typeshed import Incomplete
from collections.abc import Generator
from typing import (
    Any,
    Set,
)
from umlfri2.application.addon.dependency import AddOnDependency
from umlfri2.application.addon.license.common import CommonLicense
from umlfri2.application.addon.online.actions.installer import OnlineAddOnInstaller
from umlfri2.application.addon.online.addon import OnlineAddOn
from umlfri2.application.addon.online.location import OnlineAddOnLocation
from umlfri2.application.application import Application
from umlfri2.types.image import Image
from umlfri2.types.version import Version


class OnlineAddOnVersion:
    def __init__(
        self,
        application: Application,
        name: str,
        version: Version,
        author: str,
        homepage: str,
        license: CommonLicense,
        icon: Image,
        description: str,
        requirements: Set[AddOnDependency],
        provisions: Set[Any],
        changelog: str,
        locations: Set[OnlineAddOnLocation]
    ) -> None: ...
    @property
    def addon(self) -> OnlineAddOn: ...
    @property
    def name(self) -> str: ...
    @property
    def version(self) -> Version: ...
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
    def changelog(self): ...
    @property
    def valid_location(self) -> OnlineAddOnLocation: ...
    def install(self) -> OnlineAddOnInstaller: ...
    def update(self): ...
