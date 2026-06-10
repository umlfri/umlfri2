from PyQt5.QtGui import QMouseEvent
from typing import Optional


class ValidateTabChangeEvent:
    def __init__(self, tab_index: int) -> None: ...
    @property
    def is_valid(self) -> bool: ...


class ValidatingTabBar:
    def mousePressEvent(self, event: QMouseEvent) -> None: ...


class ValidatingTabWidget:
    def __init__(self, parent: None = ...) -> None: ...
