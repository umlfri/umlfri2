from PyQt5.QtWidgets import QSizePolicy as QSizePolicy, QWidget
from _typeshed import Incomplete
from umlfri2.types.color import Color as Color, Colors as Colors

class ColorSelectionWidget(QWidget):
    color_changed: Incomplete
    def __init__(self, btn_class=...) -> None: ...
    @property
    def selected_color(self): ...
    @selected_color.setter
    def selected_color(self, value) -> None: ...
