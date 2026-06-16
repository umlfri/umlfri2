from umlfri2.application.addon.local.gui.action import AddOnAction
from umlfri2.types.image import Image

class ToolBarItem:
    def __init__(
        self,
        action: AddOnAction,
        icon: Image,
        label: str
    ) -> None: ...
    @property
    def icon(self) -> Image: ...
    @property
    def label(self) -> str: ...
    @property
    def action(self) -> AddOnAction: ...
