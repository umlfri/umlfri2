from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QMenu,
)
from functools import partial
from typing import (
    Callable,
    Optional,
    Union,
)
from umlfri2.metamodel.diagramtype import DiagramType
from umlfri2.metamodel.elementtype import ElementType


class ContextMenu:
    def _add_menu_item(
        self,
        icon: Optional[str],
        label: str,
        shortcut: Optional[Union[str, QKeySequence.StandardKey]],
        action: Optional[Union[Callable, partial]] = ...,
        sub_menu: Optional[QMenu] = ...
    ) -> QAction: ...
    def _add_sub_menu_item(self, label: str, enabled: bool = ..., sub_menu: None = ...) -> QMenu: ...
    def _add_type_menu_item(
        self,
        type: Union[DiagramType, ElementType],
        action: Optional[Callable] = ...,
        sub_menu: Optional[QMenu] = ...,
        format: str = ...
    ) -> QAction: ...
