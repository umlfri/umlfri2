from typing import (
    Dict,
    Iterator,
    List,
)
from umlfri2.application.addon.local.addon import AddOn
from umlfri2.application.addon.local.gui.action import AddOnAction
from umlfri2.application.addon.local.gui.toolbar import ToolBar


class GuiInjection:
    def __init__(
        self,
        actions: Dict[str, AddOnAction],
        toolbars: List[ToolBar]
    ) -> None: ...
    def _set_addon(self, addon: AddOn) -> None: ...
    @property
    def toolbars(self) -> Iterator[ToolBar]: ...
