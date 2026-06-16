from .actions import AddOnStarter as AddOnStarter, AddOnStopper as AddOnStopper, AddOnUninstaller as AddOnUninstaller
from .state import AddOnState as AddOnState
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.addon import AddOnStateChangedEvent as AddOnStateChangedEvent
from typing import (
    Iterator,
    Optional,
    Set,
)
from umlfri2.application.addon.dependency import AddOnDependency
from umlfri2.application.addon.license.common import CommonLicense
from umlfri2.application.addon.local.actions.starter import AddOnStarter
from umlfri2.application.addon.local.actions.stopper import AddOnStopper
from umlfri2.application.addon.local.actions.uninstaller import AddOnUninstaller
from umlfri2.application.addon.local.gui.guiinjection import GuiInjection
from umlfri2.application.addon.local.state import AddOnState
from umlfri2.application.application import Application
from umlfri2.datalayer.storages.directory import DirectoryStorageReference
from umlfri2.metamodel.metamodel import Metamodel
from umlfri2.plugin.patch import PatchPlugin
from umlfri2.plugin.plugin import Plugin
from umlfri2.types.image import Image
from umlfri2.types.version import Version


class AddOn:
    def __init__(
        self,
        application: Application,
        storage_reference: DirectoryStorageReference,
        identifier: str,
        name: str,
        version: Version,
        author: str,
        homepage: str,
        license: CommonLicense,
        icon: Image,
        description: str,
        requirements: Set[AddOnDependency],
        provisions: Set[AddOnDependency],
        metamodel: Optional[Metamodel],
        gui_injection: Optional[GuiInjection],
        patch_plugin: Optional[PatchPlugin],
        plugin: Optional[Plugin],
        system_addon: bool
    ) -> None: ...
    @property
    def identifier(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def version(self) -> Version: ...
    @property
    def author(self): ...
    @property
    def homepage(self) -> str: ...
    @property
    def license(self): ...
    @property
    def icon(self) -> Image: ...
    @property
    def description(self) -> str: ...
    @property
    def requirements(self) -> Iterator[AddOnDependency]: ...
    @property
    def provisions(self) -> Iterator[AddOnDependency]: ...
    @property
    def metamodel(self) -> Optional[Metamodel]: ...
    @property
    def is_system_addon(self) -> bool: ...
    @property
    def application(self) -> Application: ...
    def compile(self) -> None: ...
    @property
    def state(self) -> AddOnState: ...
    @property
    def gui_injection(self) -> Optional[GuiInjection]: ...
    @property
    def storage_reference(self) -> DirectoryStorageReference: ...
    def start(self) -> AddOnStarter: ...
    def stop(self) -> AddOnStopper: ...
    def uninstall(self) -> AddOnUninstaller: ...
