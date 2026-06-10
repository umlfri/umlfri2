from typing import (
    Any,
    Iterator,
)
from umlfri2.application.drawingarea.drawingarea import DrawingArea
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow


class CanvasElementMenu:
    def __init__(
        self,
        main_window: UmlFriMainWindow,
        drawing_area: DrawingArea,
        elements: Iterator[Any]
    ) -> None: ...
