from ...constants import ADDON_NAMESPACE as ADDON_NAMESPACE, ADDON_SCHEMA as ADDON_SCHEMA
from umlfri2.application.addon.local import AddOnAction as AddOnAction, ToolBar as ToolBar, ToolBarItem as ToolBarItem
from umlfri2.types.image import Image as Image

class ToolBarLoader:
    def __init__(self, application, storage, xmlroot, actions) -> None: ...
    def load(self): ...
