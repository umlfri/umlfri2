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
    def _start(self) -> None: ...
    def _stop(self) -> None: ...
    @property
    def application(self) -> Application: ...
    def compile(self) -> None: ...
    @property
    def description(self) -> str: ...
    @property
    def gui_injection(self) -> Optional[GuiInjection]: ...
    @property
    def homepage(self) -> str: ...
    @property
    def icon(self) -> Image: ...
    @property
    def identifier(self) -> str: ...
    @property
    def is_system_addon(self) -> bool: ...
    @property
    def metamodel(self) -> Optional[Metamodel]: ...
    @property
    def name(self) -> str: ...
    @property
    def provisions(self) -> Iterator[AddOnDependency]: ...
    @property
    def requirements(self) -> Iterator[AddOnDependency]: ...
    def start(self) -> AddOnStarter: ...
    @property
    def state(self) -> AddOnState: ...
    def stop(self) -> AddOnStopper: ...
    @property
    def storage_reference(self) -> DirectoryStorageReference: ...
    def uninstall(self) -> AddOnUninstaller: ...
    @property
    def version(self) -> Version: ...
