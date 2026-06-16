from _typeshed import Incomplete
from collections.abc import Generator
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
    def reset(self) -> None: ...
    @property
    def actions(self) -> Generator[Incomplete, Incomplete]: ...
    def get_action(self, id): ...
    @property
    def toolbars(self) -> Iterator[ToolBar]: ...
