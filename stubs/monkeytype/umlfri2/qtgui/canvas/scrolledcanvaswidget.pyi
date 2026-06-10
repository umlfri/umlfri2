from PyQt5.QtGui import QWheelEvent
from typing import Union
from umlfri2.application.drawingarea.drawingarea import DrawingArea
from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.fullscreen.fullscreen import FullScreenDiagram
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow


class ScrolledCanvasWidget:
    def __init__(
        self,
        main_window: Union[FullScreenDiagram, UmlFriMainWindow],
        drawing_area: DrawingArea
    ) -> None: ...
    @property
    def diagram(self) -> Diagram: ...
    def wheelEvent(self, event: QWheelEvent) -> None: ...
