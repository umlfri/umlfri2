from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QPushButton
from typing import Type


class FontSelectionWidget:
    def __init__(self, btn_class: Type[QPushButton] = ...) -> None: ...
    def resizeEvent(self, event: QResizeEvent) -> None: ...
