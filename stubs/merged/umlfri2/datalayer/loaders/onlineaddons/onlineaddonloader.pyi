from ...constants import ONLINE_ADDON_NAMESPACE as ONLINE_ADDON_NAMESPACE, ONLINE_ADDON_SCHEMA as ONLINE_ADDON_SCHEMA
from ..textformat import format_text as format_text
from _typeshed import Incomplete
from typing import NamedTuple
from umlfri2.application.addon.dependency import AddOnDependency as AddOnDependency, AddOnDependencyType as AddOnDependencyType
from umlfri2.application.addon.license import CommonLicense as CommonLicense
from umlfri2.application.addon.online import OnlineAddOnArch as OnlineAddOnArch, OnlineAddOnHash as OnlineAddOnHash, OnlineAddOnLocation as OnlineAddOnLocation, OnlineAddOnVersion as OnlineAddOnVersion
from umlfri2.types.image import Image as Image
from umlfri2.types.version import Version as Version

class LoadedAddOnVersion(NamedTuple):
    identifier: Incomplete
    version: Incomplete

class OnlineAddOnLoader:
    def __init__(self, application, xmlroot, storage, path) -> None: ...
    def is_valid(self): ...
    def load(self): ...
