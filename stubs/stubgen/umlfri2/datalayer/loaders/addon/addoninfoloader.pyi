from ...constants import ADDON_NAMESPACE as ADDON_NAMESPACE, ADDON_SCHEMA as ADDON_SCHEMA
from ..textformat import format_text as format_text
from _typeshed import Incomplete
from typing import NamedTuple
from umlfri2.application.addon.dependency import AddOnDependency as AddOnDependency, AddOnDependencyType as AddOnDependencyType
from umlfri2.application.addon.license import CommonLicense as CommonLicense
from umlfri2.types.version import Version as Version

class AddOnInfo(NamedTuple):
    identifier: Incomplete
    name: Incomplete
    version: Incomplete
    author: Incomplete
    homepage: Incomplete
    license: Incomplete
    icon: Incomplete
    description: Incomplete
    requirements: Incomplete
    provisions: Incomplete
    metamodel: Incomplete
    injections: Incomplete
    patch_module: Incomplete
    plugin_info: Incomplete

class PluginInfo(NamedTuple):
    path: Incomplete
    starter: Incomplete

class AddOnInfoLoader:
    def __init__(self, xmlroot) -> None: ...
    def load(self): ...
