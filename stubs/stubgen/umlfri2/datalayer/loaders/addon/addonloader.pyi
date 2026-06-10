from ...constants import ADDON_ADDON_FILE as ADDON_ADDON_FILE, ADDON_DISABLE_FILE as ADDON_DISABLE_FILE, ADDON_NAMESPACE as ADDON_NAMESPACE
from .addoninfoloader import AddOnInfoLoader as AddOnInfoLoader
from .metamodel import MetamodelLoader as MetamodelLoader
from .toolbarloader import ToolBarLoader as ToolBarLoader
from umlfri2.application.addon.local import AddOn as AddOn, GuiInjection as GuiInjection
from umlfri2.datalayer.storages import DirectoryStorage as DirectoryStorage
from umlfri2.plugin import PatchPlugin as PatchPlugin, Plugin as Plugin
from umlfri2.types.image import Image as Image

class AddOnLoader:
    def __init__(self, application, storage, system_addon) -> None: ...
    def is_addon(self): ...
    def is_enabled(self): ...
    def load(self): ...
