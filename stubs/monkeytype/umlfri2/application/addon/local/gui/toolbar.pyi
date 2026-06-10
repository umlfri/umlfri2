from typing import (
    Iterator,
    List,
)
from umlfri2.application.addon.local.addon import AddOn
from umlfri2.application.addon.local.gui.toolbaritem import ToolBarItem


class ToolBar:
    def __init__(self, label: str, items: List[ToolBarItem]) -> None: ...
    def _set_addon(self, addon: AddOn) -> None: ...
    @property
    def addon(self) -> AddOn: ...
    @property
    def items(self) -> Iterator[ToolBarItem]: ...
    @property
    def label(self) -> str: ...
