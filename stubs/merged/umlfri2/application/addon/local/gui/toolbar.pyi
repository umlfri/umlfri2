from _typeshed import Incomplete
from collections.abc import Generator
from typing import (
    Iterator,
    List,
)
from umlfri2.application.addon.local.addon import AddOn
from umlfri2.application.addon.local.gui.toolbaritem import ToolBarItem


class ToolBar:
    def __init__(self, label: str, items: List[ToolBarItem]) -> None: ...
    @property
    def addon(self) -> AddOn: ...
    @property
    def id(self): ...
    @property
    def label(self) -> str: ...
    @property
    def items(self) -> Iterator[ToolBarItem]: ...
